import pandas as pd
from datetime import datetime
import os

# ======================
# CONFIGURATION
# ======================

# Name of the attendance CSV file
attendance_file = "attendance.csv"

# Path to your original student list CSV
original_file = "New_data.csv"

# Format today's date as '23 May'
today_date = datetime.today().strftime('%d %b')

# ======================
# MAIN LOGIC
# ======================

# Check if attendance file already exists
if os.path.exists(attendance_file):
    # Attendance file exists: read it
    df = pd.read_csv(attendance_file)
    print(f"Loaded existing attendance file: {attendance_file}")
else:
    # Attendance file does not exist: create it from original file
    if not os.path.exists(original_file):
        raise FileNotFoundError(f"Original file '{original_file}' not found. Please provide your student list CSV with at least 'RollNumber' and 'Name' columns.")

    original_df = pd.read_csv(original_file)
    df = original_df[["Enrolment no.", "Name"]]
    print(f"Created new attendance file from: {original_file}")

# Add today's date as a new column if it doesn't exist already
if today_date in df.columns:
    print(f"Column for '{today_date}' already exists. Nothing to do.")
else:
    df[today_date] = ""  # Or default value like 'Absent'
    print(f"Added new column '{today_date}' to attendance sheet.")

# Save the updated attendance sheet
df.to_csv(attendance_file, index=False)
print(f"Attendance file saved as: {attendance_file}")
