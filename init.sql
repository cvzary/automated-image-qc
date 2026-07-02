CREATE TABLE IF NOT EXISTS Image_Verification (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    resolution VARCHAR(50),
    status VARCHAR(50),
    rejection_reason TEXT
);