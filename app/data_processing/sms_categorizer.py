import re

class SMSCategorizer:
    def __init__(self):
        self.patterns = {
            'incoming_money': [r'received.*RWF.*from', r'You have received'],
            'payment_to_code': [r'your payment.*RWF.*to.*completed'],
            'bank_deposit': [r'bank.*deposit', r'deposit.*bank'],
            'withdrawal': [r'withdrawn.*RWF', r'You have withdrawn'],
            'transfer': [r'transfer.*RWF', r'transferred'],
            'bill_payment': [r'bill.*payment.*RWF', r'You have paid'],
            'internet/voice_bundle': [r'internet.*bundle', r'voice.*bundle', r'kugura', r'Yello!'],
        }
    
    def categorize(self, sms_body):
        # Return category based on patterns
        pass
