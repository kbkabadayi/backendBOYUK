from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors


bank = Blueprint('bank', __name__, url_prefix='/bank')

@bank.route('/addAccount', methods=['POST'])
def add():
    bank_data = request.json
    bank_account_no = bank_data['bank_account_no']
    bank_account_password = bank_data['bank_account_password']
    active = bank_data['active']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO BankAccount(bank_account_no, bank_account_password, active) VALUES (%s, %s, %s)", (bank_account_no, bank_account_password, active))

    connection.commit()
    return jsonify({"result": "Bank added"})

@bank.route('/removeAccount/<int:bank_account_no>', methods=['DELETE'])
def removeAccount(bank_account_no):
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM BankAccount WHERE bank_account_no = %s", (bank_account_no,))
    connection.commit()

    return jsonify({"result": "Bank removed"})


