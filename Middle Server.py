from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


MAIN_SERVER_URL = 'http://localhost:5000'


loan_cache = {}

@app.route('/')
def index():
    return 'Middle Server for Handling Requests'

@app.route('/get_loan_info', methods=['GET'])
def get_loan_info():
    loan_id = request.args.get('loan_id')
    if not loan_id:
        return jsonify({"error": "Loan ID is required"}), 400
    
    # Check if the loan information is in the cache
    if loan_id in loan_cache:
        return jsonify(loan_cache[loan_id]), 200
    
    # If not in cache, fetch from the main server
    response = requests.get(f'{MAIN_SERVER_URL}/get_loan_info', params={'loan_id': loan_id})
    if response.status_code == 200:
        # Cache the response
        loan_cache[loan_id] = response.json()
    
    return jsonify(response.json()), response.status_code

@app.route('/pay_loan', methods=['POST'])
def pay_loan():
    data = request.json
    loan_id = data.get('loan_id')
    payment_amount = data.get('payment_amount')
    
    if not loan_id or not payment_amount:
        return jsonify({"error": "Loan ID and payment amount are required"}), 400
    
    # Forward the request to the main server
    response = requests.post(f'{MAIN_SERVER_URL}/pay_loan', json=data)
    
    if response.status_code == 200:
        # If payment is successful, update the cache
        updated_loan_info = response.json().get('updated_loan_info')
        if updated_loan_info:
            loan_cache[loan_id] = updated_loan_info
    
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5001)
