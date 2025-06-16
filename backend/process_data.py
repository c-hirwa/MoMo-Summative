import xml.etree.ElementTree as ET
import re
import logging
import os
from datetime import datetime
from database import SMSDatabase

# Configure logging
logging.basicConfig(
    filename='processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SMSProcessor:
    def __init__(self):
        self.db = SMSDatabase()
        self.processed_count = 0
        self.error_count = 0

        # Transaction type patterns
        self.patterns = {
            'incoming_money': [
                r'You have received (\d+(?:\.\d+)?) RWF from (.+?)\.',
                r'received (\d+(?:\.\d+)?) RWF from (.+?)[\.\s]'
            ],
            'payment_completed': [
                r'Your payment of (\d+(?:\.\d+)?) RWF to (.+?) has been completed',
                r'payment of (\d+(?:\.\d+)?) RWF to (.+?) has been completed'
            ],
            'airtime_payment': [
                r'payment of (\d+(?:\.\d+)?) RWF to Airtime',
                r'(\d+(?:\.\d+)?) RWF.*?Airtime.*?completed'
            ],
            'agent_withdrawal': [
                r'You (.+?) have via agent: (.+?) \((\d+)\), withdrawn (\d+(?:\.\d+)?) RWF',
                r'withdrawn (\d+(?:\.\d+)?) RWF.*?agent'
            ],
            'internet_bundle': [
                r'purchased an internet bundle.*?(\d+(?:\.\d+)?) RWF',
                r'internet bundle.*?(\d+(?:\.\d+)?) RWF'
            ],
            'bank_transfer': [
                r'bank.*?(\d+(?:\.\d+)?) RWF',
                r'(\d+(?:\.\d+)?) RWF.*?bank'
            ]
        }

    def extract_transaction_id(self, message):
        patterns = [
            r'Transaction ID: (\w+)',
            r'TxId: (\w+)',
            r'TxId:(\w+)',
            r'ID: (\w+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def extract_date(self, message):
        patterns = [
            r'Date: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
            r'on (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
        ]
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                try:
                    return datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                except:
                    continue
        return None

    def extract_fee(self, message):
        fee_match = re.search(r'Fee: (\d+(?:\.\d+)?) RWF', message, re.IGNORECASE)
        return float(fee_match.group(1)) if fee_match else 0.0

    def categorize_message(self, message):
        message = message.strip()
        for trans_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    return self.build_transaction_data(trans_type, match, message)
        return None

    def build_transaction_data(self, trans_type, match, message):
        transaction_id = self.extract_transaction_id(message)
        date_time = self.extract_date(message)
        fee = self.extract_fee(message)

        amount = 0.0
        sender_name = None
        receiver_name = None
        phone_number = None
        agent_name = None
        agent_phone = None

        if trans_type == 'incoming_money':
            amount = float(match.group(1))
            sender_name = match.group(2).strip()
            trans_type = 'Incoming Money'
        elif trans_type == 'payment_completed':
            amount = float(match.group(1))
            receiver_name = match.group(2).strip()
            trans_type = 'Payment Completed'
        elif trans_type == 'airtime_payment':
            amount = float(match.group(1))
            receiver_name = 'Airtime'
            trans_type = 'Airtime Payment'
        elif trans_type == 'agent_withdrawal':
            if len(match.groups()) >= 4:
                sender_name = match.group(1).strip()
                agent_name = match.group(2).strip()
                agent_phone = match.group(3)
                amount = float(match.group(4))
            else:
                amount = float(match.group(1))
            trans_type = 'Agent Withdrawal'
        elif trans_type == 'internet_bundle':
            amount = float(match.group(1))
            receiver_name = 'Internet Bundle'
            trans_type = 'Internet Bundle'
        elif trans_type == 'bank_transfer':
            amount = float(match.group(1))
            trans_type = 'Bank Transfer'

        return (
            transaction_id, trans_type, amount, fee, sender_name,
            receiver_name, phone_number, agent_name, agent_phone,
            date_time, message
        )

    def process_xml_file(self, xml_file_path):
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            sms_elements = root.findall('sms')

            logging.info(f"Starting to process XML file: {xml_file_path}")

            for sms in sms_elements:
                body_text = sms.attrib.get('body')
                if body_text:
                    message = body_text.strip()
                    transaction_data = self.categorize_message(message)
                    if transaction_data:
                        if self.db.insert_transaction(transaction_data):
                            self.processed_count += 1
                            logging.info(f"Processed transaction: {transaction_data[1]}")
                        else:
                            self.error_count += 1
                            self.db.log_error(message, "Database insertion failed")
                    else:
                        self.error_count += 1
                        self.db.log_error(message, "Could not categorize message")
                        logging.warning(f"Could not categorize: {message[:50]}...")

            logging.info(f"Processing complete. Processed: {self.processed_count}, Errors: {self.error_count}")
            print(f"Processing complete!")
            print(f"Successfully processed: {self.processed_count} messages")
            print(f"Errors/Unprocessed: {self.error_count} messages")

        except Exception as e:
            logging.error(f"Error processing XML file: {e}")
            print(f"Error processing file: {e}")

def main():
    processor = SMSProcessor()
    processor.process_xml_file('data/modified_sms_v2.xml')

if __name__ == "__main__":
    main()
