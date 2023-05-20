from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors


illness = Blueprint('illness', __name__, url_prefix='/illness')
@illness.route('/add', methods=['GET','POST'])
def add():

    illness_data = request.json
    illness_name = illness_data['illness_name']
    type = illness_data['type']
    patient_TCK = illness_data['TCK']


    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute( "SELECT illness_name FROM Illness  ")
    cursor.execute("INSERT INTO Illness(hospital_id, name, city) VALUES (%s, %s, %s)", ())

    connection.commit()
    return illness_data
