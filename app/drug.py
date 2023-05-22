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
    restock_date = datetime.now()

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    for drug_name, count in drug_to_count.items():
        cursor.execute("UPDATE HasDrug SET drug_count = drug_count + %s WHERE drug_name = %s AND pharmacy_id = %s", (count, drug_name, pharm_id))
        connection.commit()
        cursor.execute("INSERT INTO Restocks VALUES (%s, %s, %s, %s, %s)", (pharm_id, warehouse_id, drug_name, count, restock_date))
        connection.commit()

    return jsonify({"result": "Drug restocked to the pharmacy"})

@drug.route('/orderDrug', methods=['POST'])
def orderDrug():
    data = request.json
    drug_to_count = data["drug_to_count"]
    pharm_id = data["pharm_id"]
    bank_account_no = data["bank_account_no"]
    patient_TCK = data["patient_TCK"]
    order_date = datetime.now()

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    for drug_name, count in drug_to_count.items():
        cursor.execute("SELECT needs_prescription FROM Drug WHERE name = %s", (drug_name,))
        requires = cursor.fetchone()['needs_prescription']
        if requires.lower() == 'yes':
            cursor.execute("SELECT drug_name FROM Contains WHERE presc_id in (SELECT presc_id FROM Prescribes WHERE patient_TCK = %s)", patient_TCK)
            drugs_prescribed = cursor.fetchall()
            if drug_name not in drugs_prescribed:
                return jsonify({"result": "Order contains a drug patient is not prescribed"})



        cursor.execute("UPDATE HasDrug SET drug_count = drug_count - %s WHERE drug_name = %s AND pharmacy_id = %s", (count, drug_name, pharm_id))
        connection.commit()

        status = "pompa"
        cursor.execute("INSERT INTO Orders VALUES (%s, %s, %s, %s, %s, %s)", (bank_account_no, patient_TCK, drug_name, order_date, count, status))
        connection.commit()

        # cursor.execute("SELECT * FROM Cart WHERE TCK = %s AND drug_name = %s", (patient_TCK, drug_name))
        # exist = cursor.fetchone()

        # if exist is None:
        #     cursor.execute("INSERT INTO Cart VALUES (%s, %s, %s)", (patient_TCK, drug_name, count))
        #     connection.commit()
        # else:
        #     cursor.execute("UPDATE Cart SET drug_count = drug_count + %s WHERE TCK = %s AND drug_name = %s", (count, patient_TCK,drug_name))
        #     connection.commit()

        cursor.execute("SELECT price FROM Drug where name = %s", (drug_name,))
        price = cursor.fetchone()
        offset = count * price['price']

        cursor.execute("UPDATE BankAccount SET balance = balance - %s WHERE bank_account_no = %s", (offset, bank_account_no))
        connection.commit()

    return jsonify({"result": "Drug ordered from"})







