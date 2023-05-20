from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors
from datetime import datetime


drug = Blueprint('drug', __name__, url_prefix='/drug')

@drug.route('/registerDrug', methods=['POST'])
def add():
    data = request.json
    drug_id = data["drug_id"]
    name = data["name"]
    needs_prescription = data["needs_prescription"]
    drug_class = data["drug_class"]
    drug_type = data["drug_type"]
    price = data["price"]

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO Drug VALUES (%s, %s, %s, %s, %s, %s)", (drug_id, name, needs_prescription, drug_class, drug_type, price))

    connection.commit()
    return jsonify({"result": "Drug added"})


@drug.route('/pharmacyAddDrug', methods=['POST'])
def add():
    data = request.json
    drug_id = data["drug_id"]
    pharm_id = data["pharm_id"]
    warehouse_id = data["warehouse_id"]
    restock_date = datetime.datetime.now()

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO HasDrug VALUES (%s, %s)", (drug_id, pharm_id))

    cursor.execute("INSER INTO Restocks VALUES (%s, %s, %s, %s)", (pharm_id, warehouse_id, drug_id, restock_date))
    

    connection.commit()
    return jsonify({"result": "Drug added to the pharmacy"})






