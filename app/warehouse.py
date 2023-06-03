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

    return "Warehouse added successfully"

@warehouse.route('/remove/<int:id>', methods = ['GET', 'POST'])
def remove(id):
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM PharmaceuticalWarehouse WHERE warehouse_id = %s", [id])

    connection.commit()
    return "Warehouse removed sueccessfully"
    

@warehouse.route('/listRestocks', methods=['GET'])
def show():
    data = request.json
    pharm_id = data["pharm_id"]
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM Restocks WHERE pharm_id = %s", (pharm_id,))
    return jsonify(cursor.fetchall())