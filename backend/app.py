from flask import Flask, jsonify, request
from flask_cors import CORS
from database import SMSDatabase
import json

app = Flask(__name__)
CORS(app)

db = SMSDatabase()

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions with optional filtering"""
    try:
        transactions = db.get_all_transactions()
        
        # Apply filters if provided
        transaction_type = request.args.get('type')
        search_term = request.args.get('search')
        
        if transaction_type:
            transactions = [t for t in transactions if t['transaction_type'] == transaction_type]
        
        if search_term:
            transactions = [t for t in transactions 
                          if search_term.lower() in (t['raw_message'] or '').lower()]
        
        return jsonify({
            'success': True,
            'data': transactions,
            'count': len(transactions)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get summary statistics"""
    try:
        stats = db.get_summary_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/transaction-types', methods=['GET'])
def get_transaction_types():
    """Get unique transaction types"""
    try:
        transactions = db.get_all_transactions()
        types = list(set([t['transaction_type'] for t in transactions if t['transaction_type']]))
        
        return jsonify({
            'success': True,
            'data': sorted(types)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
