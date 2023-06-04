from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors
import json

cart = Blueprint('cart', __name__, url_prefix='/cart')

@cart.route('/addToCart', methods=['POST'])
def pay():
    cart_data = request.json
    patient_TCK = cart_data["patient_TCK"]
    drug_name = cart_data["drug_name"]
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Cart WHERE TCK = %s AND drug_name = %s", (patient_TCK, drug_name))
    exist = cursor.fetchone()

    if exist is None:
        cursor.execute("INSERT INTO Cart VALUES (%s, %s, 1)", (patient_TCK, drug_name))
        connection.commit()
    else:
        cursor.execute("UPDATE Cart SET drug_count = drug_count + 1 WHERE TCK = %s AND drug_name = %s", ( patient_TCK,drug_name))
        connection.commit()
    return jsonify({"result": "Drug added to cart"})

@cart.route('/removeFromCart', methods=['POST'])
def decrement():
    cart_data = request.json
    patient_TCK = cart_data["patient_TCK"]
    drug_name = cart_data["drug_name"]
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Cart WHERE TCK = %s AND drug_name = %s", (patient_TCK, drug_name ))
    exist = cursor.fetchone()

    if exist["drug_count"] == 1:
        cursor.execute("DELETE FROM Cart WHERE TCK = %s AND drug_name = %s", (patient_TCK,drug_name))
        connection.commit()

    else:
        cursor.execute("UPDATE Cart SET drug_count = drug_count - 1 WHERE TCK = %s AND drug_name = %s", ( patient_TCK,drug_name))
        connection.commit()

    return jsonify({"result": "Drug decremented from cart"})


@cart.route('/show', methods = ['POST'])
def show():
    data = request.json
    TCK = data["patient_TCK"]
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM CartView WHERE TCK = %s", (TCK,))
    return jsonify(cursor.fetchall())

