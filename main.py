from fastapi import FastAPI, UploadFile, File, HTTPException
import cv2
import numpy as np
import psycopg2
import os

app = FastAPI(title="Image Dataset Validator API")

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )

@app.post("/validate/")
async def validate_image(file: UploadFile = File(...)):
    status = "ACCEPTED"
    reason = "None"
    resolution = "Unknown"

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        status = "REJECTED"
        reason = "Corrupted file or not an image format"
    else:
        height, width, _ = img.shape
        resolution = f"{width}x{height}"
        if width < 200 or height < 200:
            status = "REJECTED"
            reason = "Resolution too low"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Image_Verification (file_name, resolution, status, rejection_reason)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (file.filename, resolution, status, reason))
        
        inserted_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {
        "id": inserted_id,
        "file_name": file.filename,
        "status": status,
        "resolution": resolution,
        "reason": reason
    }