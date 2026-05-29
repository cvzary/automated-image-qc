import os
import shutil
import sqlite3
import cv2

input_dir = "input_data"
accepted_dir = "accepted_data"
rejected_dir = "rejected_data"

for directory in [input_dir, accepted_dir, rejected_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

if not os.listdir(input_dir):
    print(f"Info: The folder '{input_dir}' is currently empty.")
    print(f"Please put some test images into '{input_dir}' and run the script again!\n")
    print("Execution stopped: No files to analyze.")
    exit()


db_connection = sqlite3.connect("verification_logs.db")
cursor = db_connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Image_Verification (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               file_name TEXT,
               resolution TEXT,
               status TEXT,
               rejection_reason TEXT
               )        
               """)
db_connection.commit()

for file_name in os.listdir(input_dir):
    file_path = os.path.join(input_dir, file_name)

    status = "ACCEPTED"
    reason = "None"
    resolution = "Unknown"
    target_dir = accepted_dir

    img = cv2.imread(file_path)

    if img is None:
        status = "REJECTED"
        reason = "Corrupted file or not an image format"
        resolution = "Unknown"
        target_dir = rejected_dir
    else:
        height, width, _ = img.shape
        resolution = f"{width}x{height}"

        if width < 200 or height < 200:
            status = "REJECTED"
            reason = "Resolution too low"
            target_dir = rejected_dir

    cursor.execute("""
        INSERT INTO Image_Verification (file_name, resolution, status, rejection_reason)
        VALUES (?, ?, ?, ?)
                   """, (file_name, resolution, status, reason))
    
    shutil.move(file_path, os.path.join(target_dir, file_name))

db_connection.commit()

print("DATABASE ERROR REPORT")
cursor.execute("SELECT file_name, rejection_reason FROM Image_Verification WHERE status = 'REJECTED'")

rejected_files = cursor.fetchall()
if rejected_files:
    for file in rejected_files:
        print(f"File: {file[0]} | Reason: {file[1]}")
else:
    print("No rejected files in the latest batch.")

db_connection.close()
