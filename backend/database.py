import sqlite3
import logging
from datetime import datetime

class SMSDatabase:
    def __init__(self, db_path='sms_database.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT UNIQUE,
                transaction_type TEXT NOT NULL,
                amount REAL,
                fee REAL DEFAULT 0,
                sender_name TEXT,
                receiver_name TEXT,
                phone_number TEXT,
                agent_name TEXT,
                agent_phone TEXT,
                date_time DATETIME,
                raw_message TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Error log table for unprocessed messages
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS error_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_message TEXT,
                error_reason TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_transaction(self, transaction_data):
        """Insert a single transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO transactions 
                (transaction_id, transaction_type, amount, fee, sender_name, 
                 receiver_name, phone_number, agent_name, agent_phone, 
                 date_time, raw_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', transaction_data)
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error inserting transaction: {e}")
            return False
        finally:
            conn.close()
    
    def log_error(self, message, error_reason):
        """Log unprocessed messages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO error_logs (raw_message, error_reason)
            VALUES (?, ?)
        ''', (message, error_reason))
        
        conn.commit()
        conn.close()
    
    def get_all_transactions(self):
        """Get all transactions for API"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM transactions ORDER BY date_time DESC')
        rows = cursor.fetchall()
        
        columns = [description[0] for description in cursor.description]
        transactions = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return transactions
    
    def get_summary_stats(self):
        """Get summary statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total transactions by type
        cursor.execute('''
            SELECT transaction_type, COUNT(*) as count, SUM(amount) as total_amount
            FROM transactions 
            GROUP BY transaction_type
        ''')
        type_stats = cursor.fetchall()
        
        # Monthly stats
        cursor.execute('''
            SELECT strftime('%Y-%m', date_time) as month, 
                   COUNT(*) as count, SUM(amount) as total_amount
            FROM transactions 
            WHERE date_time IS NOT NULL
            GROUP BY strftime('%Y-%m', date_time)
            ORDER BY month
        ''')
        monthly_stats = cursor.fetchall()
        
        conn.close()
        return {
            'type_stats': type_stats,
            'monthly_stats': monthly_stats
        }
