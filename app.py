from flask import Flask, request, jsonify, render_template
import csv
import pandas as pd
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

current_user = {
    'name': '',
    'enroll': '',
    'total_working_days': 0,
    'present': 0,
    'last_attendance_date': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify({'message': 'Expected JSON'}), 400
    data = request.get_json()
    enroll_input = data.get('enrolment_no', '').strip()
    password_input = data.get('password', '').strip()

    try:
        with open('New_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Enrolment no.'].strip() == enroll_input and row['Password'].strip() == password_input:
                    current_user['name'] = row['Name'].strip() if 'Name' in row else 'Unknown'
                    current_user['enroll'] = enroll_input
                    current_user['total_working_days'] = 0
                    current_user['present'] = 0
                    current_user['last_attendance_date'] = None
                    return jsonify({'message': 'Login successful'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        print('Error:', e)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/admin')
def admin():
    return render_template('admin_login.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/api/user-info')
def user_info():
    if not current_user['enroll']:
        return jsonify({'message': 'Not logged in'}), 401
    return jsonify({
        'name': current_user['name'],
        'enroll': current_user['enroll'],
        'total_working_days': current_user['total_working_days'],
        'present': current_user['present']
    })

@app.route('/api/mark-attendance', methods=['POST'])
def mark_attendance():
    if not current_user['enroll']:
        return jsonify({'message': 'Not logged in'}), 401

    today_str = datetime.today().strftime('%d %b')  # e.g., "03 Jul"

    try:
        with open('attendance.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            fieldnames = reader.fieldnames if reader.fieldnames else []

        if today_str not in fieldnames:
            fieldnames.append(today_str)
            for row in rows:
                row[today_str] = ""

        found = False
        for row in rows:
            if row['Enrolment no.'].strip() == current_user['enroll']:
                row[today_str] = "P"
                found = True
                break

        if not found:
            return jsonify({'message': 'User not found in attendance file'}), 404

        with open('attendance.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        if current_user['last_attendance_date'] == today_str:
            return jsonify({'message': 'Attendance already marked today!'}), 400

        current_user['total_working_days'] = len([col for col in fieldnames if col not in ('RollNumber', 'Name', 'Enrolment no.')])
        current_user['present'] += 1
        current_user['last_attendance_date'] = today_str

        return jsonify({
            'total_working_days': current_user['total_working_days'],
            'present': current_user['present'],
            'message': 'Attendance marked successfully!'
        })

    except FileNotFoundError:
        return jsonify({'message': 'Attendance file not found'}), 500
    except Exception as e:
        print('Error:', e)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/admin-login', methods=['POST'])
def admin_login():
    if not request.is_json:
        return jsonify({'message': 'Expected JSON'}), 400
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if username == 'adminiitr' and password == '0000':
        return jsonify({'message': 'Admin login successful'}), 200
    else:
        return jsonify({'message': 'Invalid admin credentials'}), 401

@app.route('/analysis/<date>')
def attendance_analysis(date):
    try:
        df = pd.read_csv('attendance.csv')

        if date not in df.columns:
            return f"<h3>No attendance data found for date: {date}</h3>", 404

        present_df = df[df[date] == 'P']

        # ✅ Build a dict with keys matching analysis.html template
        present_students = [
            {'name': row['Name'], 'enroll': row['Enrolment no.']}
            for _, row in present_df.iterrows()
        ]

        return render_template(
            'analysis.html',
            date=date,
            present_students=present_students
        )

    except Exception as e:
        print("Error in analysis route:", e)
        return "<h3>Internal server error</h3>", 500

if __name__ == '__main__':
    app.run(debug=True)
