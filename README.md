# Image Dataset Validator API

An automated, containerized REST API designed for the initial quality control (sanity check) and validation of image datasets. Built with **FastAPI**, **OpenCV**, and **PostgreSQL**, this project simulates a modern backend microservice for Machine Learning data pipelines, ensuring data integrity before feeding images into ML models.

### Key Features

* **RESTful API:** Upload images directly via HTTP POST requests. Includes an auto-generated, interactive Swagger UI documentation for easy testing.
* **In-Memory Processing:** Analyzes files directly in RAM using `numpy` and `cv2.imdecode`, eliminating the need for temporary disk storage.
* **Corrupted File Detection:** Uses OpenCV to identify and filter out corrupted files or invalid image formats.
* **Resolution Validation:** Enforces a minimum resolution constraint (200x200 pixels) to prevent low-quality inputs.
* **PostgreSQL Logging:** Records verification history, image dimensions, and specific rejection reasons using parameterized queries for maximum security.
* **Containerized Architecture:** Fully isolated, reproducible, and ready-to-deploy environment using **Docker** and **Docker Compose**.

### Tech Stack

* **Language:** Python 3.10
* **Framework:** FastAPI, Uvicorn
* **Libraries:** `opencv-python-headless`, `numpy`, `psycopg2-binary`, `python-multipart`
* **Database:** PostgreSQL 15
* **Infrastructure:** Docker, Docker Compose

---

### Installation & Setup

Thanks to Docker, you don't need to install Python, PostgreSQL, or any libraries on your local machine.

1. **Clone the repository:**
```bash
git clone https://github.com/cvzary/automated-image-qc.git
cd automated-image-qc
```

2. **Run the application:**
Ensure you have Docker Desktop running, then execute:
```bash
docker compose up --build
```

3. **Access the API:**
Once the containers are up, open your browser and navigate to the interactive Swagger UI:
👉 **http://localhost:8000/docs**

*From there, you can expand the `POST /validate/` endpoint, click "Try it out", and upload test images directly from your browser.*

---

### Database Schema

The PostgreSQL database (`validator_db`) is automatically initialized on the first run. It contains the `Image_Verification` table with the following structure:

* `id` *(SERIAL, Primary Key)* * `file_name` *(VARCHAR)* - Name of the uploaded file.
* `resolution` *(VARCHAR)* - Dimensions formatted as WidthxHeight.
* `status` *(VARCHAR)* - ACCEPTED or REJECTED.
* `rejection_reason` *(TEXT)* - Details on why the file failed validation (if applicable).
