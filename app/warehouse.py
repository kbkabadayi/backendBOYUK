from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors

warehouse = Blueprint('warehouse', __name__, url_prefix='/warehouse')

@warehouse.route('/add', methods = ['GET', 'POST'])
def add():
    data = request.json

    warehouse_id = data['warehouse_id']
    warehouse_name = data['warehouse_name']
    warehouse_city = data['warehouse_city']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO PharmaceuticalWarehouse(warehouse_id, warehouse_name, warehouse_city) VALUES(%s, %s, %s)", (warehouse_id, warehouse_name, warehouse_city))

    connection.commit()

    return "success"

@warehouse.route('/remove/<int:id>', methods = ['GET', 'POST'])
def remove(id):
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM PharmaceuticalWarehouse WHERE warehouse_id = %s", [id])

    connection.commit()
    return "success"


@warehouse.route('/listRestocks', methods=['POST','GET'])
def show():
    data = request.json
    warehouse_id = data["warehouse_id"]
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM RestockView WHERE warehouse_id = %s", (warehouse_id,))
    return jsonify(cursor.fetchall())

@warehouse.route('/getWarehouses', methods=['GET'])
def showarehouses():
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT warehouse_id, warehouse_name FROM PharmaceuticalWarehouse")
    return jsonify(cursor.fetchall())
