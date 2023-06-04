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
    return "success"

@pharmacy.route('/remove/<int:id>', methods = ['GET', 'POST', 'DELETE'])
def remove(id):
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM Pharmacy WHERE pharmacy_id = %s", [id])
    connection.commit()

    return "success"

@pharmacy.route('/list', methods = ['POST'])
def listall():
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute( "SELECT pharm_name, pharm_city FROM Pharmacy")
    pharm_data = cursor.fetchall()
    return jsonify(pharm_data)

@pharmacy.route('/all', methods = ['GET', 'POST'])
def listAllUsers():
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * From Pharmacy")    
    return jsonify(cursor.fetchall())