from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors
from datetime import datetime

analysis = Blueprint('anaylsis', __name__, url_prefix='/analysis')

@analysis.route('/createDrugAnalysis', methods = ['GET','POST'])
def create_drug_analysis():
    data = request.json
    will_be_created = data['create']
    patient_TCK = data['patient_TCK']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    if will_be_created == "yes":
        cursor.execute('SELECT drug_name, COUNT(*) AS drug_count FROM Orders WHERE patient_TCK = %s GROUP BY drug_name ORDER BY drug_count DESC LIMIT 1', (patient_TCK,))
        result = cursor.fetchone()

        if result is not None:
            drug_name = result[0]
            order_count = result[1]

            analysis_data = {
                "drug_name": drug_name,
                "order_count": order_count
            }

            return jsonify(analysis_data)
        
        else:
            return "No ordered drugs"

@analysis.route('/createDoctorAnalysis', methods = ['GET','POST'])
def create_doctor_analysis():
    data = request.json
    will_be_created = data['create']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    if will_be_created == "yes":
        cursor.execute('SELECT doctor_TCK, COUNT(*) AS doctor_count FROM Prescribes GROUP BY doctor_TCK ORDER BY doctor_count DESC LIMIT 1')
        result = cursor.fetchone()

        if result is not None:
            doctor_TCK = result[0]
            doctor_count = result[1] # number of occurences

            cursor.execute('SELECT fullname FROM User WHERE TCK = %s', (doctor_TCK,))
            doctor_data = cursor.fetchone()['fullname']

            doctor_analysis_data = {
                "doctor_fullname": doctor_data,
                "presc_count": doctor_count
            }

            return jsonify(doctor_analysis_data)

        else:
            return "Error no doctor"
