from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import traceback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///billing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Unpaid")

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.String(20), nullable=False)
    bill = db.relationship('Bill', backref=db.backref('payments', lazy=True))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/bills', methods=['POST'])
def create_bill():
    bill_data = request.get_json()
    bill = Bill(
        patient_id=bill_data['patient_id'],
        amount=bill_data['amount']
    )
    db.session.add(bill)
    db.session.commit()
    return jsonify({
        'id': bill.id,
        'patient_id': bill.patient_id,
        'amount': bill.amount,
        'status': bill.status
    }), 201

@app.route('/get-amounts', methods=['POST'])
def get_amount():
    data = request.get_json()
    bill_id = data['billId']
    bill = Bill.query.get(bill_id)
    if bill:
        return jsonify({
            'amount': bill.amount            
        })
    else:
        return jsonify({'error': 'Bill not found'}), 404


@app.route('/bills/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    bill = Bill.query.get(bill_id)
    if bill:
        return jsonify({
            'id': bill.id,
            'patient_id': bill.patient_id,
            'amount': bill.amount,
            'status': bill.status
        })
    else:
        return jsonify({'error': 'Bill not found'}), 404

@app.route('/payments', methods=['POST'])
def process_payment():
    payment_data = request.get_json()
    bill = Bill.query.get(payment_data['bill_id'])
    if bill and bill.status == "Unpaid":
        if float(payment_data['amount']) == float(bill.amount):
            payment = Payment(
                bill_id=payment_data['bill_id'],
                amount=payment_data['amount'],
                payment_date=payment_data['payment_date']
            )
            bill.status = "Paid"
            db.session.add(payment)
            db.session.commit()
            return jsonify({
                'message': 'Payment processed',
                'bill_id': payment.bill_id,
                'amount': payment.amount,
                'payment_date': payment.payment_date
            }), 201
        else:
            return jsonify({'error': 'Payment amount does not match bill amount'}), 400
    else:
        return jsonify({'error': 'Bill not found or already paid'}), 404

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
