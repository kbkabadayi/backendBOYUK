from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors
from datetime import datetime

analysis = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis.route('/createDrugAnalysis', methods = ['GET','POST'])
def create_drug_analysis():
    data = request.json
    patient_TCK = data['patient_TCK']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT drug_name, COUNT(*) AS drug_count FROM Orders WHERE patient_TCK = %s GROUP BY drug_name ORDER BY drug_count DESC LIMIT 1', (patient_TCK,))
    result = cursor.fetchone()

    if result is not None:
        drug_name = result[0]['drug_name']
        order_count = result[1]['order_count']

        analysis_data = {
            "drug_name": drug_name,
            "order_count": order_count
        }

        return jsonify(analysis_data)
    
    else:
        return "No ordered drugs"

@analysis.route('/createDoctorAnalysis', methods = ['GET','POST'])
def create_doctor_analysis():
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT doctor_TCK, COUNT(*) AS doctor_count FROM Prescribes GROUP BY doctor_TCK ORDER BY doctor_count DESC LIMIT 1')
    result = cursor.fetchone()

    if result is not None:
        doctor_TCK = result[0]['doctor_TCK']
        doctor_count = result[1]['doctor_count'] # number of occurences

        cursor.execute('SELECT fullname FROM User WHERE TCK = %s', (doctor_TCK,))
        doctor_data = cursor.fetchone()

        if doctor_data is not None:
            doctor_full_name = doctor_data['fullname']

            doctor_analysis_data = {
                "doctor_fullname": doctor_full_name,
                "presc_count": doctor_count
            }

            return jsonify(doctor_analysis_data)

    else:
        return "Error no doctor"

@analysis.route('/createMoneyAnalysis', methods = ['GET','POST'])
def create_money_analysis():
    data = request.json
    patient_TCK = data['patient_TCK']
    last_months = 5

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    today = datetime.date.today()
    months_ago = today - datetime.timedelta(days = 30 * last_months)
    cursor.execute('SELECT drug_name, count, order_date FROM Orders WHERE patient_TCK = %s AND order_date >= %s', (patient_TCK, months_ago))
    orders = cursor.fetchall()

    total_spent = 0

    for order in orders:
        drug_name = order[0]['drug_name']
        count = order[1]['count']
        
        cursor.execute('SELECT price FROM Drug WHERE name = %s', (drug_name,))
        drug_price = cursor.fetchone()['price']
        
        total_spent += drug_price * count

    average_spent = total_spent / last_months

    average_spent_object = {
        "average_spent": average_spent
    }

    return jsonify(average_spent_object)