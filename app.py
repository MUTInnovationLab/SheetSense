from flask import Flask, render_template, send_from_directory, url_for, request
import os
os.environ['GOOGLE_CLOUD_PROJECT'] = 'cvsystem-253f9'
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore, storage
import json
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DatetimeWithNanoseconds):
            return obj.isoformat()
        return super().default(obj)

app = Flask(__name__)

# Initialize Firebase using environment variables
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': os.getenv('GOOGLE_CLOUD_PROJECT')
})
db = firestore.client()

def fetch_students():
    student_list_ref = db.collection('students').document('students_list_id')
    student_list_doc = student_list_ref.get()
    if student_list_doc.exists:
        student_list_data = student_list_doc.to_dict()
        student_list_df = pd.DataFrame(student_list_data['students'])
        return student_list_df
    return pd.DataFrame()

def fetch_weekly_reports():
    weekly_reports_ref = db.collection('weekly')
    weekly_reports_docs = weekly_reports_ref.stream()
    weekly_reports = []
    
    for doc in weekly_reports_docs:
        weekly_report_data = doc.to_dict()
        if 'students' in weekly_report_data:
            weekly_reports.append(weekly_report_data['students'])
    
    return weekly_reports

def fetch_monthly_reports():
    monthly_reports_ref = db.collection('monthly')
    monthly_reports_docs = monthly_reports_ref.stream()
    monthly_reports = []
    
    for doc in monthly_reports_docs:
        monthly_report_data = doc.to_dict()
        if 'students' in monthly_report_data:
            monthly_reports.append(monthly_report_data['students'])
    
    return monthly_reports

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view_reports')
def view_reports():
    student_list_df = fetch_students()
    weekly_reports = fetch_weekly_reports()
    monthly_reports = fetch_monthly_reports()
    
    # Combine weekly and monthly reports
    combined_reports = weekly_reports + monthly_reports
    
    # Extract emails from student list
    student_emails = student_list_df['email'].tolist()
    
    # Initialize lists for submitted and not submitted students
    submitted_students = []
    not_submitted_students = []
    
    # Compare emails and categorize students
    for student in student_list_df.to_dict(orient='records'):
        if any(student['email'] in report for report in combined_reports):
            submitted_students.append(student)
        else:
            not_submitted_students.append(student)
    
    return render_template('reports.html', submitted=submitted_students, not_submitted=not_submitted_students)

@app.route('/view_history')
def view_history():
    return render_template('history.html')

@app.route('/manage_files', methods=['GET', 'POST'])
def manage_files():
    if request.method == 'POST':
        file = request.files['student_file']
        if file:
            # Save file to Firebase Storage
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            file_path = f'students/{timestamp}_{file.filename}'
            upload_task = storage.child(file_path).put(file)
            upload_task.add_done_callback(upload_complete_callback)
            return 'File uploaded successfully!'
    return render_template('files.html')

def upload_complete_callback(task):
    download_url = task.result()
    print(f'File uploaded to {download_url}')

@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)
