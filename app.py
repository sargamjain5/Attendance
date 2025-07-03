from flask import Flask, request, jsonify, render_template
import csv
from flask_cors import CORS
from datetime import datetime  # ✅ Needed for date check

app = Flask(__name__)
CORS(app)

# Temporary in-memory storage of current user
current_user = {
    'name': '',
    'enroll': '',
    'total_working_days': 0,
    'present': 0,
    'last_attendance_date': None  # ✅ Track last attendance date
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
                    current_user['last_attendance_date'] = None  # reset on login
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

    today_str = datetime.today().strftime('%Y-%m-%d')
    if current_user['last_attendance_date'] == today_str:
        return jsonify({'message': 'Attendance already marked today!'}), 400

    # Update attendance if not marked today
    current_user['total_working_days'] += 1
    current_user['present'] += 1
    current_user['last_attendance_date'] = today_str

    return jsonify({
        'total_working_days': current_user['total_working_days'],
        'present': current_user['present'],
        'message': 'Attendance marked successfully!'
    })

if __name__ == '__main__':
    app.run(debug=True)
