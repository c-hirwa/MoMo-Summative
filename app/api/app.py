from flask import Flask, jsonify, request
from flask_cors import CORS
from db_operations import DatabaseManager

app = Flask(__name__)
CORS(app)
db = DatabaseManager('../data/sms_database.db')

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    category = request.args.get('category')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Query database and return JSON
    pass

@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    # Return transaction summaries, totals, etc.
    pass

@app.route('/api/analytics/monthly', methods=['GET'])
def get_monthly_analytics():
    # Return monthly transaction data
    pass
