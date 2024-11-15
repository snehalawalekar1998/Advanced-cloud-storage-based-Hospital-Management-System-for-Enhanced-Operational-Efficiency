from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
from functools import wraps
from flask_cors import CORS
import json
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
CORS(app)
# Mock database
users = {}
appointments = []
doctors = [
    {"id": 1, "name": "Dr. John Doe", "specialization": "Cardiologist"},
    {"id": 2, "name": "Dr. Alice Green", "specialization": "Dermatologist"},
    {"id": 3, "name": "Dr. Robert White", "specialization": "Pediatrician"},
    {"id": 4, "name": "Dr. Emily Black", "specialization": "Orthopedic"}
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            flash("Username already taken.", "danger")
            return redirect(url_for('register'))
        
        users[username] = {
            "password": password,
            "profile": {"name": "", "age": "", "contact": "", "email": ""}
        }
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('index.html', show_register=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.get(username)
        if user and user['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))
    
    return render_template('index.html', show_login=True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    username = session.get('username')
    if username not in users:
        flash("User not found", "danger")
        return redirect(url_for('login'))

    profile = users[username]['profile']
    return render_template('index.html', profile=profile, appointments=appointments, doctors=doctors)

@app.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    username = session['username']
    users[username]['profile'] = {
        "name": request.form['name'],
        "age": request.form['age'],
        "contact": request.form['contact'],
        "email": request.form['email']
    }
    flash("Profile updated successfully!", "success")
    return redirect(url_for('home'))

@app.route('/appointments/schedule', methods=['POST'])
@login_required
def schedule_appointment():
    doctor_id = int(request.form['doctor_id'])
    username = request.form['patient_name']
    print("Username is")
    print(username)
    doctor = next((doc for doc in doctors if doc["id"] == doctor_id), None)
    if doctor:
        appointment = {
            "id": len(appointments) + 1,
            "doctor_id": doctor['id'],
            "name": doctor['name'],
            "specialization": doctor['specialization'],
            "date": request.form['date'],
            "time": request.form['time']
        }
        appointments.append(appointment)
        flash("Appointment scheduled successfully!", "success")
        updateDoctorService(appointment,username)

                
    return redirect(url_for('home'))

def updateDoctorService(appointment,username):
    appintment_data = {
        "id": appointment["id"],
        "doctor_id": appointment["doctor_id"],
        "patient_name": username,
        "date": appointment['date'],
        "time": appointment['time']
    }

    # Send the appointment to the doctor service
    doctor_service_url = 'http://localhost:5002/api/appointments'  # Replace with actual doctor service address
    try:        
        response = requests.post(doctor_service_url, json=appintment_data)
        response.raise_for_status()  # Raises an error if the request was unsuccessful
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
        print(f"Response text: {response.text}")  # Show server's response    
    return

@app.route('/appointments/delete/<int:appointment_id>')
@login_required
def delete_appointment(appointment_id):
    global appointments
    appointments = [a for a in appointments if a["id"] != appointment_id]
    flash("Appointment deleted successfully!", "info")
    return redirect(url_for('home'))

@app.route('/appointments/edit/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    appointment = next((a for a in appointments if a["id"] == appointment_id), None)
    if not appointment:
        flash("Appointment not found", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        appointment["date"] = request.form["date"]
        appointment["time"] = request.form["time"]
        flash("Appointment updated successfully!", "success")
        return redirect(url_for('home'))

    return render_template('index.html', profile=users[session['username']]['profile'], appointments=appointments, edit_appointment=appointment, doctors=doctors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
