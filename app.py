from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "careconnect-secret-key"

# SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///careconnect.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =================================================
# DATABASE MODELS
# =================================================

class Patient(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    age = db.Column(db.Integer)

    gender = db.Column(db.String(20))

    phone = db.Column(db.String(20))

    blood_group = db.Column(db.String(10))

    location = db.Column(db.String(150))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Appointment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    patient_name = db.Column(
        db.String(100),
        nullable=False
    )

    date = db.Column(
        db.String(20),
        nullable=False
    )

    time = db.Column(
        db.String(20),
        nullable=False
    )

    purpose = db.Column(
        db.String(200)
    )

    status = db.Column(
        db.String(30),
        default="Scheduled"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class AmbulanceRequest(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    requester = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    pickup = db.Column(
        db.String(200)
    )

    destination = db.Column(
        db.String(200)
    )

    urgency = db.Column(
        db.String(30)
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class BloodRequest(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    requester = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    blood_group = db.Column(
        db.String(10)
    )

    units = db.Column(
        db.Integer
    )

    location = db.Column(
        db.String(200)
    )

    status = db.Column(
        db.String(30),
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/")
def dashboard():

    total_patients = Patient.query.count()

    total_appointments = Appointment.query.count()

    pending_ambulances = AmbulanceRequest.query.filter_by(
        status="Pending"
    ).count()

    active_blood_requests = BloodRequest.query.filter_by(
        status="Active"
    ).count()

    appointments = Appointment.query.order_by(
        Appointment.date,
        Appointment.time
    ).limit(5).all()

    ambulance_requests = AmbulanceRequest.query.filter_by(
        status="Pending"
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        total_patients=total_patients,
        total_appointments=total_appointments,
        pending_ambulances=pending_ambulances,
        active_blood_requests=active_blood_requests,
        appointments=appointments,
        ambulance_requests=ambulance_requests
    )


# =====================================================
# PATIENTS
# =====================================================

@app.route("/patients")
def patients():

    search = request.args.get("search", "")

    if search:

        patient_list = Patient.query.filter(
            (Patient.name.ilike(f"%{search}%")) |
            (Patient.phone.ilike(f"%{search}%"))
        ).all()

    else:

        patient_list = Patient.query.order_by(
            Patient.id.desc()
        ).all()

    return render_template(
        "patients.html",
        patients=patient_list,
        search=search
    )


@app.route("/patients/add", methods=["POST"])
def add_patient():

    patient = Patient(

        name=request.form["name"],

        age=request.form["age"],

        gender=request.form["gender"],

        phone=request.form["phone"],

        blood_group=request.form["blood_group"],

        location=request.form["location"]

    )

    db.session.add(patient)

    db.session.commit()

    flash(
        "Patient registered successfully!",
        "success"
    )

    return redirect(url_for("patients"))


# =====================================================
# APPOINTMENTS
# =====================================================

@app.route("/appointments")
def appointments():

    appointment_list = Appointment.query.order_by(
        Appointment.date,
        Appointment.time
    ).all()

    return render_template(
        "appointments.html",
        appointments=appointment_list
    )


@app.route("/appointments/add", methods=["POST"])
def add_appointment():

    appointment = Appointment(

        patient_name=request.form["patient_name"],

        date=request.form["date"],

        time=request.form["time"],

        purpose=request.form["purpose"],

        status="Scheduled"

    )

    db.session.add(appointment)

    db.session.commit()

    flash(
        "Appointment booked successfully!",
        "success"
    )

    return redirect(url_for("appointments"))


@app.route(
    "/appointments/status/<int:id>",
    methods=["POST"]
)
def update_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    appointment.status = request.form["status"]

    db.session.commit()

    flash(
        "Appointment status updated.",
        "success"
    )

    return redirect(url_for("appointments"))


# =====================================================
# AMBULANCE
# =====================================================

@app.route("/ambulance")
def ambulance():

    requests = AmbulanceRequest.query.order_by(
        AmbulanceRequest.id.desc()
    ).all()

    return render_template(
        "ambulance.html",
        requests=requests
    )


@app.route("/ambulance/add", methods=["POST"])
def add_ambulance():

    ambulance = AmbulanceRequest(

        requester=request.form["requester"],

        phone=request.form["phone"],

        pickup=request.form["pickup"],

        destination=request.form["destination"],

        urgency=request.form["urgency"],

        status="Pending"

    )

    db.session.add(ambulance)

    db.session.commit()

    flash(
        "Ambulance request submitted.",
        "success"
    )

    return redirect(url_for("ambulance"))


@app.route(
    "/ambulance/status/<int:id>",
    methods=["POST"]
)
def update_ambulance(id):

    ambulance = AmbulanceRequest.query.get_or_404(id)

    ambulance.status = request.form["status"]

    db.session.commit()

    flash(
        "Ambulance request updated.",
        "success"
    )

    return redirect(url_for("ambulance"))


# =====================================================
# BLOOD REQUESTS
# =====================================================

@app.route("/blood")
def blood():

    blood_group = request.args.get(
        "blood_group",
        ""
    )

    location = request.args.get(
        "location",
        ""
    )

    query = BloodRequest.query

    if blood_group:

        query = query.filter_by(
            blood_group=blood_group
        )

    if location:

        query = query.filter(
            BloodRequest.location.ilike(
                f"%{location}%"
            )
        )

    blood_requests = query.order_by(
        BloodRequest.id.desc()
    ).all()

    return render_template(
        "blood.html",
        blood_requests=blood_requests,
        blood_group=blood_group,
        location=location
    )


@app.route("/blood/add", methods=["POST"])
def add_blood():

    blood_request = BloodRequest(

        requester=request.form["requester"],

        phone=request.form["phone"],

        blood_group=request.form["blood_group"],

        units=request.form["units"],

        location=request.form["location"],

        status="Active"

    )

    db.session.add(blood_request)

    db.session.commit()

    flash(
        "Blood requirement submitted.",
        "success"
    )

    return redirect(url_for("blood"))


@app.route(
    "/blood/status/<int:id>",
    methods=["POST"]
)
def update_blood(id):

    blood_request = BloodRequest.query.get_or_404(id)

    blood_request.status = request.form["status"]

    db.session.commit()

    flash(
        "Blood request updated.",
        "success"
    )

    return redirect(url_for("blood"))


# =====================================================
# FACILITIES
# =====================================================

@app.route("/facilities")
def facilities():

    facility_list = [

        {
            "name": "City Care Hospital",
            "type": "Hospital",
            "location": "Pune, Maharashtra",
            "phone": "020-12345678"
        },

        {
            "name": "City Blood Bank",
            "type": "Blood Bank",
            "location": "Pune, Maharashtra",
            "phone": "020-87654321"
        },

        {
            "name": "Community Health Clinic",
            "type": "Clinic",
            "location": "Pune, Maharashtra",
            "phone": "020-45678912"
        }

    ]

    return render_template(
        "facilities.html",
        facilities=facility_list
    )


# =====================================================
# CREATE DATABASE
# =====================================================

with app.app_context():

    db.create_all()


# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
