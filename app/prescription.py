from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors
from datetime import datetime

prescription = Blueprint('pharmacy', __name__, url_prefix='/prescription')

@prescription.route('/addPresc', methods = ['GET', 'POST'])
def add():
    data = request.json

    presc_id = data['presc_id']
    date = datetime.now()

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("INSERT INTO Prescription VALUES(%s, %s)", (presc_id, date))

    connection.commit()

    return "Prescription is added successfully"

@prescription.route('/prescribe', methods = ['GET', 'POST'])
def prescribe():
    data = request.json

    doctor_TCK = data['doctor_TCK']
    patient_TCK = data['patient_TCK']
    presc_id = data['presc_id']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("INSERT INTO Prescribes VALUES(%s, %s, %s)", (doctor_TCK, patient_TCK, presc_id))

    connection.commit()

    return "Prescription is written to patient successfully"