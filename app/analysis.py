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

@analysis.route('createPharmacyAnalysis', methods = ['GET','POST'])
def create_pharmacy_analysis():
    data = request.json
    will_be_created = data['create']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    # if will_be_created == "yes":

