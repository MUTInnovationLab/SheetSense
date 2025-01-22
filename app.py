from flask import Flask, render_template, send_from_directory
import os
import pandas as pd
from firebase_admin import credentials, firestore, storage, initialize_app

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase.
cred = credentials.Certificate("config/serviceAccountKey.json") 
initialize_app(cred) 
db = firestore.client()

# Fetch data from Firestore 
def fetch_data(collection):
    try:
        docs = db.collection(collection).stream()
        data = [doc.to_dict() for doc in docs]
        print(f"Fetched data from {collection}: {data}")
        return data
    except Exception as e:
        print(f"Error fetching data from {collection}: {e}")
        return []


# Process data 
def process_data():
    student_list = fetch_data('students')
    weekly_reports = fetch_data('weekly')
    monthly_reports = fetch_data('monthly')

    print(f"Student List: {student_list}") # Debugging statement
    print(f"Weekly Reports: {weekly_reports}") # Debugging statement
    print(f"Monthly Reports: {monthly_reports}") # Debugging statement

    submitted = []
    not_submitted = []

    for student in student_list:
        try:
            print(f"Processing student: {student}")  # Debugging statement
            student_number = student.get('student number', 'Unknown')
            firstname = student.get('firstname', 'Unknown')
            lastname = student.get('lastname', 'Unknown')
            
            if student_number != 'Unknown':
                weekly_submitted = next((report for report in weekly_reports if report.get('student number') == student_number), None)
                monthly_submitted = next((report for report in monthly_reports if report.get('student number') == student_number), None)
                
                if weekly_submitted and monthly_submitted:
                    submitted.append({
                        'student_number': student_number,
                        'student_name': f"{firstname} {lastname}",
                        'report_title': 'Weekly and Monthly Reports',
                        'date_submitted': f"{weekly_submitted['date']}, {monthly_submitted['date']}"
                    })
                else:
                    not_submitted.append({
                        'student_number': student_number,
                        'student_name': f"{firstname} {lastname}",
                        'report_title': 'Not Submitted',
                        'status': 'Pending'
                    })
            else:
                print(f"Student record missing 'student number': {student}")  # Debugging statement
        except Exception as e:
            print(f"Error processing student: {e}")

    print(f"Submitted students: {submitted}") # Debugging statement
    print(f"Not submitted students: {not_submitted}") # Debugging statement
    
    return submitted, not_submitted


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view_reports') 
def view_reports(): 
    submitted, not_submitted = process_data() 
    return render_template('Reports.html', submitted=submitted, not_submitted=not_submitted)

@app.route('/view_history')
def view_history():
    return render_template('history.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)
