from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors
from datetime import datetime


drug = Blueprint('drug', __name__, url_prefix='/drug')

@drug.route('/registerDrug', methods=['POST'])
def registerDrug():
    data = request.json
    name = data["name"]
    needs_prescription = data["needs_prescription"]
    drug_class = data["drug_class"]
    drug_type = data["drug_type"]
    price = data["price"]

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO Drug VALUES (%s, %s, %s, %s, %s)", (name, needs_prescription, drug_class, drug_type, price))

    connection.commit()
    return jsonify({"result": "Drug added"})


@drug.route('/restockDrug', methods=['POST'])
def restockDrug():
    data = request.json
    drug_to_count = data["drug_to_count"]
    pharm_id = data["pharm_id"]
    warehouse_id = data["warehouse_id"]
    restock_date = datetime.datetime.now()

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    for drug_name, count in drug_to_count:
        cursor.execute("UPDATE HasDrug SET drug_count = drug_count + %s WHERE drug_name = %s AND pharm_id = %s", (count, drug_name, pharm_id))
        connection.commit()
        cursor.execute("INSERT INTO Restocks VALUES (%s, %s, %s, %s, %s)", (pharm_id, warehouse_id, drug_name, count, pharm_id, restock_date))
        connection.commit()
    
    return jsonify({"result": "Drug restocked to the pharmacy"})

@drug.route('/orderDrug', methods=['POST'])
def orderDrug():
    data = request.json
    drug_to_count = data["drug_to_count"]
    bank_account_no = data["bank_account_no"]
    patient_TCK = data["patient_TCK"]
    order_date = datetime.now()

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    for drug_name, count in drug_to_count:
        cursor.execute("UPDATE HasDrug SET drug_count = drug_count + %s WHERE drug_name = %s AND pharm_id = %s", (count, drug_name, pharm_id))
        connection.commit()
        cursor.execute("INSERT INTO Restocks VALUES (%s, %s, %s, %s, %s)", (pharm_id, warehouse_id, drug_name, count, pharm_id, restock_date))
        connection.commit()
    
    return jsonify({"result": "Drug restocked in pharmacy"})







