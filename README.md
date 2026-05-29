# Image Dataset Validator

An automated Python tool designed for the initial quality control (sanity check) and validation of image datasets. Built using **OpenCV** for digital image analysis and **SQLite** for relational database logging.

This project simulates a backend utility for an Image Recognition maintenance environment, ensuring data integrity before feeding images into machine learning models.

## Key Features
- **Directory Automation:** Automatically detects, creates, and manages input/output directories.
- **Corrupted File Detection:** Uses OpenCV (`cv2.imread`) to identify and filter out corrupted files or invalid formats.
- **Resolution Validation:** Enforces a minimum resolution constraint (200x200 pixels) to prevent low-quality inputs.
- **SQL Database Logging:** Records verification history, image dimensions, and specific rejection reasons using parameterized queries for maximum security.
- **Error Reporting:** Generates a quick console report of all rejected files upon execution.

## Tech Stack
- **Language:** Python 3.x
- **Libraries:** OpenCV (`opencv-python`), `sqlite3`, `shutil`, `os`
- **Database:** SQLite

## Installation & Setup

1. **Clone the repository:**
   git clone [https://github.com/cvzary/automated-image-qc.git](https://github.com/cvzary/automated-image-qc.git)
   cd Automated-Image-QC

2. **Install requirements:**
    pip install opencv-python

3. **Run the application:**
    python validator.py

## Database Schema
The local SQLite database (verification_logs.db) contains the **Image_Verification** table with the following structure:

*id (INTEGER, Primary Key, Autoincrement)*

*file_name (TEXT) - Name of the validated file.*

*resolution (TEXT) - Dimensions formatted as WidthxHeight.*

*status (TEXT) - ACCEPTED or REJECTED.*

*rejection_reason (TEXT) - Details on why the file failed validation (if applicable).*
