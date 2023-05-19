from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors


hospital = Blueprint('hospital', __name__, url_prefix='/hospital')

@hospital.route('/add', methods=['GET','POST'])
def add():

    hospital_data = request.json
    hospital_id = hospital_data['hospital_id']
    name = hospital_data['name']
    city = hospital_data['city']


    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO Hospital(hospital_id, name, city) VALUES (%s, %s, %s)", (hospital_id, name, city))

    connection.commit()
    return hospital_data

