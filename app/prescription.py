from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors
from datetime import datetime

prescription = Blueprint('prescription', __name__, url_prefix='/prescription')

@prescription.route('/prescribe', methods = ['GET', 'POST'])
def prescribe():
    data = request.json

    doctor_TCK = data['doctor_TCK']
    patient_TCK = data['patient_TCK']
    drug_name = data['drug_name']
    illness = data['illness']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("INSERT INTO Prescription(date, illness) VALUES( %s, %s)", ( date, illness))
    connection.commit()

    cursor.execute("SELECT presc_id FROM Prescription WHERE date = %s ", (date,))
    connection.commit()
    presc_id_data = cursor.fetchall()
    presc_id = presc_id_data[0]["presc_id"]
    cursor.execute("INSERT INTO Prescribes(presc_id, doctor_TCK, patient_TCK) VALUES(%s, %s, %s)", (presc_id, doctor_TCK, patient_TCK))
    connection.commit()

    cursor.execute("INSERT INTO Contains VALUES(%s, %s)", (presc_id, drug_name))
    connection.commit()

    return jsonify("success")


@prescription.route('/listPrescriptions', methods = ['GET', 'POST'])
def pampito():
    data = request.json
    doctor_TCK = data['doctor_TCK']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute("SELECT * FROM Prescription NATURAL JOIN Prescribes NATURAL JOIN Contains JOIN User ON patient_TCK = TCK WHERE doctor_TCK = %s ", (doctor_TCK,))
    return jsonify(cursor.fetchall())
