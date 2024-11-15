from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps

from flask_cors import CORS


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
CORS(app)

# Sample doctor profile data
doctor_profile = [
    {"id": 1, "username": "John", "name": "Dr. John Doe", "specialization": "Cardiologist", "experience": "15 years", "contact": "123-456-7890", "email": "jane.smith@hospital.com"},
    {"id": 2, "username": "Alice", "name": "Dr. Alice Green", "specialization": "Dermatologist", "experience": "20 years", "contact": "123-456-7890", "email": "alice.green@hospital.com"},
    {"id": 3, "username": "Robert", "name": "Dr. Robert White", "specialization": "Pediatrician", "experience": "11 years", "contact": "123-456-7890", "email": "robert.white@hospital.com"},
    {"id": 4, "username": "Emily", "name": "Dr. Emily Black", "specialization": "Orthopedic", "experience": "12 years", "contact": "123-456-7890", "email": "emily.black@hospital.com"}
]

# Sample appointments data
#appointments = [
#    {"id": 1, "doctor_id": 1, "patient_name": "John Doe", "date": "2023-10-28", "time": "10:00 AM"},
#    {"id": 2, "doctor_id": 2, "patient_name": "Jane Roe", "date": "2023-10-29", "time": "11:00 AM"},
#    {"id": 3, "doctor_id": 3, "patient_name": "Testing", "date": "2023-10-29", "time": "11:00 AM"}
#]
appointments = []

# Sample login credentials
credentials = [
    {"doc_id": 1, "username": "John", "password": "Doe"},
    {"doc_id": 2, "username": "Alice", "password": "Green"},
    {"doc_id": 3, "username": "Robert", "password": "White"},
    {"doc_id": 4, "username": "Emily", "password": "Black"}
]

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Please log in first", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        # Check credentials
        for credential in credentials:
            if username == credential['username'] and password == credential['password']:
                session['logged_in'] = True
                session['username'] = username  # Store logged-in doctor username
                flash("Logged in successfully!", "success")
                return redirect(url_for('index'))
       
        flash("Invalid username or password", "danger")
        return redirect(url_for('login'))
   
    return render_template('index.html', show_login=True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)  # Clear the stored username
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    doctor_data = next((doc for doc in doctor_profile if doc['username'] == session['username']), None)
    
    if doctor_data is None:
        flash("Doctor profile not found", "danger")
        return redirect(url_for('logout'))  # Redirect to logout or another appropriate page
    
    print("doctor login")
    print(appointments)
    doctor_appointments = [apt for apt in appointments if apt['doctor_id'] == doctor_data['id']]
    return render_template('index.html', profile=doctor_data, appointments=doctor_appointments)


@app.route('/appointments/delete/<int:appointment_id>')
@login_required
def delete_appointment(appointment_id):
    global appointments
    appointments = [a for a in appointments if a["id"] != appointment_id]
    return redirect(url_for('index'))

@app.route('/appointments/edit/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    appointment = next((a for a in appointments if a["id"] == appointment_id), None)
    if not appointment:
        return redirect(url_for('index'))

    if request.method == 'POST':
        appointment["patient_name"] = request.form["patient_name"]
        appointment["date"] = request.form["date"]
        appointment["time"] = request.form["time"]
        return redirect(url_for('index'))

    return render_template('index.html', profile=doctor_profile, appointments=appointments, edit_appointment=appointment)
# In doctor service (app.py)

# Doctor service - app.py

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    if 'logged_in' not in session:
        return jsonify({"error": "User not logged in"}), 401

    # Get the logged-in doctor's username
    username = session['username']
    doctor_data = next((doc for doc in doctor_profile if doc['username'] == username), None)
    print("doctor data")
    print(doctor_data)

    if not doctor_data:
        return jsonify({"error": "Doctor profile not found"}), 404

    doctor_id = doctor_data['id']
    
    # Filter appointments for the logged-in doctor
    doctor_appointments = [apt for apt in appointments if apt['doctor_id'] == doctor_id]

    return jsonify({'appointments': doctor_appointments})

@app.route('/api/appointments', methods=['POST'])
def add_appointment():
    try:
        new_appointment = request.get_json()
        print("Received appointment data:", new_appointment)  # Log the data
        
        # Ensure data is in the expected format
        if not new_appointment:
            print("testing doctor 0 *******************************")
            return jsonify({"error": "No JSON data received"}), 400
        if "doctor_id" not in new_appointment or "date" not in new_appointment or "time" not in new_appointment:
            print("testing doctor 1 *******************************")
            return jsonify({"error": "Missing required appointment fields"}), 400
        
        # Add the appointment to the list
        print("testing doctor 2 *******************************")
        appointments.append(new_appointment)
        print("testing doctor 3 *******************************")
        print(appointments)
        # Return the updated list of appointments
        return jsonify({'appointments': appointments}), 201
    
    except Exception as e:
        print("Error:", str(e))  # Log any errors
        return jsonify({"error": "An error occurred"}), 500


"""@app.route('/view-appointments', methods=['GET'])
def viewAppointments():
    print("entered view appointments function")
    print(appointments)
    output_message = appointments
    # Respond with the processed information
    return jsonify({
        "output": output_message,        
    })"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)