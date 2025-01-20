from flask import Flask, render_template, send_from_directory, url_for
import os
os.environ['GOOGLE_CLOUD_PROJECT'] = 'sheetsensedb'
import firebase_admin 
from firebase_admin import credentials, firestore 
import pandas as pd
import json
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds

class CustomJSONEncoder(json.JSONEncoder): 
    def default(self, obj): 
        if isinstance(obj, DatetimeWithNanoseconds): 
            return obj.isoformat() 
        return super().default(obj)

app = Flask(__name__)

# Print the GOOGLE_CLOUD_PROJECT environment variable for debugging
print("GOOGLE_CLOUD_PROJECT:", os.getenv('GOOGLE_CLOUD_PROJECT'))

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
    submitted_students = []
    
    for doc in weekly_reports_docs:
        weekly_report_data = doc.to_dict()
        
        # Debugging statement to check the structure of each document
        print(json.dumps(weekly_report_data, indent=2, cls=CustomJSONEncoder))
        
        # Check if 'students' key exists in the document
        if 'students' in weekly_report_data:
            weekly_report_df = pd.DataFrame(weekly_report_data['students'])
            submitted_students.extend(weekly_report_df['email'].tolist())
        else:
            print(f"Document {doc.id} does not contain 'students' key.")
    
    return set(submitted_students)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view_reports')
def view_reports():
    student_list_df = fetch_students() 
    submitted_students = fetch_weekly_reports() 
    
    student_list_df['status'] = student_list_df['email'].apply(lambda x: 'Submitted' if x in submitted_students else 'Not Submitted') 
    
    submitted_df = student_list_df[student_list_df['status'] == 'Submitted'] 
    not_submitted_df = student_list_df[student_list_df['status'] == 'Not Submitted'] 
    
    return render_template('reports.html', submitted=submitted_df.to_dict(orient='records'), not_submitted=not_submitted_df.to_dict(orient='records'))

@app.route('/view_history')
def view_history():
    return render_template('history.html')

@app.route('/manage_files')
def manage_files():
    return render_template('files.html')

@app.route('/static/<path:filename>') 
def custom_static(filename): 
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)