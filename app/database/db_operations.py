import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        # Create tables from schema
        pass
    
    def insert_transaction(self, transaction_data):
        # Insert parsed transaction
        pass
    
    def get_transactions_by_category(self, category):
        # Query transactions
        pass
