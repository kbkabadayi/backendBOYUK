from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors


illness = Blueprint('illness', __name__, url_prefix='/illness')

@illness.route('/add', methods=['GET','POST'])
def add():

    illness_data = request.json
    illness_name = illness_data["illness_name"]
    type = illness_data["type"]
    patient_TCK = illness_data["patient_TCK"]

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute( "SELECT illness_name FROM Illness WHERE illness_name = %s", (illness_name,))
    exist = cursor.fetchone()
    if exist is None:
        cursor.execute("INSERT INTO Illness(illness_name, type) VALUES (%s, %s)", (illness_name, type))
        connection.commit()
    cursor.execute("INSERT INTO HasIllness(patient_TCK, illness_name) VALUES (%s, %s)", (patient_TCK, illness_name))
    connection.commit()
    return "ok"
