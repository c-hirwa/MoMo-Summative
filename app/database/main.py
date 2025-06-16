from xml_parser import SMSParser
from sms_categorizer import SMSCategorizer
from db_operations import DatabaseManager
import logging

def main():
    # Set up logging
    logging.basicConfig(filename='processing.log', level=logging.INFO)
    
    # Initialize components
    parser = SMSParser('data/sms_data.xml')
    categorizer = SMSCategorizer()
    db = DatabaseManager('data/sms_database.db')
    
    # Process data
    sms_messages = parser.parse_xml()
    
    for sms in sms_messages:
        try:
            category = categorizer.categorize(sms['body'])
            # Clean and insert data
            db.insert_transaction(processed_sms)
        except Exception as e:
            logging.error(f"Failed to process SMS: {e}")