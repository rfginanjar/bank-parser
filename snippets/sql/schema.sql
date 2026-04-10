CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE, hashed_password VARCHAR(255), created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE transactions (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), bank_name VARCHAR(100), amount DECIMAL(10,2), type VARCHAR(10), category VARCHAR(50), date DATE, file_id INT, ocr_text TEXT, status VARCHAR(20) DEFAULT 'pending');
CREATE TABLE files (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), filename VARCHAR(255), path TEXT, uploaded_at TIMESTAMP DEFAULT NOW());
CREATE TABLE ocr_results (id SERIAL PRIMARY KEY, file_id INT REFERENCES files(id), engine VARCHAR(50), raw_text TEXT, confidence FLOAT, processed_at TIMESTAMP DEFAULT NOW());
CREATE TABLE pending_reviews (id SERIAL PRIMARY KEY, transaction_id INT REFERENCES transactions(id), reason VARCHAR(255), created_at TIMESTAMP DEFAULT NOW());
