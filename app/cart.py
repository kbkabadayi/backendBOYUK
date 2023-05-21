from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors
import json

cart = Blueprint('cart', __name__, url_prefix='/cart')

@cart.route('/pay<int:TCK>', methods=['DELETE'])
def pay(TCK):
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM Cart WHERE TCK = %s", (TCK,))
    connection.commit()

@cart.route('show<int:TCK>', methods = ['GET'])
def show(TCK):
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Cart WHERE TCK = %s", (TCK,))
    result = json.dumps(cursor.fetchall())
    return result

