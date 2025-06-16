CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id VARCHAR(50),
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2),
    sender_name VARCHAR(100),
    receiver_name VARCHAR(100),
    transaction_date DATETIME,
    fee DECIMAL(10,2),
    raw_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE,
    description TEXT
);

CREATE TABLE processing_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    error_type VARCHAR(50),
    processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
