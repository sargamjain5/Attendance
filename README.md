# 🎓 IIT Roorkee NCC Attendance Portal

A web-based attendance management system for IIT Roorkee’s NCC cadets and administrators. This portal allows students to securely mark their daily attendance and provides admins with an easy-to-use dashboard to analyze attendance records by date.

---

## 🚀 Features

✅ Secure **student login** using enrollment number and password  
✅ Dedicated **admin login** with hardcoded credentials (`adminiitr` / `0000`)  
✅ Prevents duplicate attendance marking on the same day  
✅ Updates attendance records in a CSV file automatically  
✅ Admin can view a list of students present on a specific date  
✅ Responsive, modern interface  
✅ Built with **Flask**, **HTML**, **CSS**, and **JavaScript**

---


## 🔑 Login Credentials

### ✅ Student Login
- **Enrollment No. & Password:** Use the credentials stored in `New_data.csv` (each student's enrollment number and password).

### ✅ Admin Login
- **Username:** adminiitr  
- **Password:** 0000

## 🚀 How to Run
1. Install requirements:
   ```bash
   pip install flask pandas flask-cors
