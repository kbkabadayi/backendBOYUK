from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors

pharmacy = Blueprint('pharmacy', __name__, url_prefix='/pharmacy')

@pharmacy.route('/add', methods = ['GET', 'POST'])
def add():
    data = request.json

    pharm_id = data['pharmacy_id']
    pharm_name = data['pharm_name']
    pharm_city = data['pharm_city']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO Pharmacy(pharmacy_id, pharm_name, pharm_city) VALUES (%s, %s, %s)", (pharm_id, pharm_name, pharm_city))

    connection.commit()
    return data

@pharmacy.route('/remove/<int:id>', methods = ['GET', 'POST', 'DELETE'])
def remove(id):
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM Pharmacy WHERE pharmacy_id = %s", [id])
    connection.commit()

    return "Pharmacy removed successfully"


@pharmacy.route('/addHasDrug', methods = ['GET', 'POST'])
def addHasDrug():
    data = request.json

    drug_id = data['drug_id']
    pharmacy_id = data['pharmacy_id']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("INSERT INTO HasDrug(drug_id, pharmacy_id) VALUES(%s, %s)", (drug_id, pharmacy_id))
    connection.commit()

    return "Drug is added to has drug table successfully"