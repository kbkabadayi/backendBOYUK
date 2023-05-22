from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors


bank = Blueprint('bank', __name__, url_prefix='/bank')

@bank.route('/addAccount', methods=['POST'])
def add():
    bank_data = request.json
    bank_account_no = bank_data['bank_account_no']
    bank_account_password = bank_data['bank_account_password']
    patient_TCK = bank_data['patient_TCK']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO BankAccount VALUES (%s, %s, 'deactive', 5000, %s)", (bank_account_no, bank_account_password, patient_TCK))

    connection.commit()
    return jsonify({"result": "Bank added"})

@bank.route('/removeAccount', methods=['POST'])
def removeAccount():
    data = request.json
    bank_account_no = data['bank_account_no']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM BankAccount WHERE bank_account_no = %s", (bank_account_no,))
    connection.commit()

    return jsonify({"result": "Bank removed"})


@bank.route('/setActive', methods=['PUT'])
def setActive():
    data = request.json
    bank_account_no = data['bank_account_no']
    patient_TCK = data['patient_TCK']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    deactive = 'deactive'
    active = 'active'

    cursor.execute("UPDATE BankAccount SET active = %s WHERE patient_TCK = %s", (deactive, patient_TCK,))
    connection.commit()

    cursor.execute("UPDATE BankAccount SET active = %s WHERE bank_account_no = %s", (active, bank_account_no,))
    connection.commit()

    return jsonify({"result": "Bank removed"})

@bank.route('/listAccounts', methods=['POST'])
def listAcc():
    data = request.json
    patient_TCK = data['patient_TCK']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM BankAccount WHERE patient_TCK = %s", (patient_TCK,))
    banks = cursor.fetchall()

    return jsonify(banks)


