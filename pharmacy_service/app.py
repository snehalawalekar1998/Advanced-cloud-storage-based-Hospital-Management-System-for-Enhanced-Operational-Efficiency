from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmacy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Medication and Order models
class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Pending")

# Initialize database if not already initialized
with app.app_context():
    db.create_all()

# Route to render HTML interface
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Endpoint to add a new medication
@app.route('/medications', methods=['POST'])
def add_medication():
    data = request.get_json()
    if 'name' not in data or 'stock' not in data or 'price' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        new_med = Medication(name=data['name'], stock=data['stock'], price=data['price'])
        db.session.add(new_med)
        db.session.commit()
        return jsonify({'id': new_med.id, 'name': new_med.name}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Medication could not be added due to a database error'}), 500

# Endpoint to retrieve medication details by ID
@app.route('/medications/<int:id>', methods=['GET'])
def get_medication(id):
    med = Medication.query.get(id)
    if med:
        return jsonify({'id': med.id, 'name': med.name, 'stock': med.stock, 'price': med.price})
    return jsonify({'error': 'Medication not found'}), 404

# Endpoint to update medication stock and price
@app.route('/medications/<int:id>', methods=['PUT'])
def update_medication(id):
    data = request.get_json()
    med = Medication.query.get(id)
    if med:
        med.stock = data.get('stock', med.stock)
        med.price = data.get('price', med.price)
        db.session.commit()
        return jsonify({'id': med.id, 'name': med.name, 'stock': med.stock, 'price': med.price})
    return jsonify({'error': 'Medication not found'}), 404

# Endpoint to place a medication order
@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    med = Medication.query.get(data['medication_id'])
    if med and med.stock >= data['quantity']:
        new_order = Order(patient_id=data['patient_id'], medication_id=data['medication_id'], quantity=data['quantity'])
        med.stock -= data['quantity']  # Reduce stock based on order quantity
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'order_id': new_order.id, 'status': new_order.status}), 201
    return jsonify({'error': 'Medication not available or insufficient stock'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004)