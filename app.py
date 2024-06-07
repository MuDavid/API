from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Mock database
loans = {
    "1001": {
        "user_name": "John Doe",
        "loan_status": "Active",
        "amount_due": 1500.75,
        "due_date": "2024-07-01"
    },
    "1002": {
        "user_name": "Jane Smith",
        "loan_status": "Paid",
        "amount_due": 0.0,
        "due_date": None
    },
    # Add more loan entries as needed
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_loan_info', methods=['GET'])
def get_loan_info():
    loan_id = request.args.get('loan_id')
    
    if not loan_id:
        return jsonify({"error": "Loan ID is required"}), 400
    
    loan_info = loans.get(loan_id)
    
    if not loan_info:
        return jsonify({"error": "Loan not found"}), 404
    
    return jsonify(loan_info), 200

@app.route('/pay_loan', methods=['POST'])
def pay_loan():
    data = request.json
    loan_id = data.get('loan_id')
    payment_amount = data.get('payment_amount')
    
    if not loan_id or not payment_amount:
        return jsonify({"error": "Loan ID and payment amount are required"}), 400
    
    loan_info = loans.get(loan_id)
    
    if not loan_info:
        return jsonify({"error": "Loan not found"}), 404

    # Update the loan information
    if loan_info['loan_status'] == 'Paid':
        return jsonify({"message": "Loan is already paid"}), 400
    
    loan_info['amount_due'] -= payment_amount
    if loan_info['amount_due'] <= 0:
        loan_info['amount_due'] = 0
        loan_info['loan_status'] = 'Paid'
        loan_info['due_date'] = None
    
    return jsonify({"message": "Payment successful", "updated_loan_info": loan_info}), 200

if __name__ == '__main__':
    app.run(debug=True)
