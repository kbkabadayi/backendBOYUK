from flask import Blueprint, jsonify, request, session
from database import get_connection
import MySQLdb.cursors


user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/add', methods=['GET','POST'])
def add():
    user_data = request.json
    TCK = user_data["TCK"]
    password = user_data["password"]
    fullname = user_data["fullname"]
    address = user_data["address"]
    birth_year = user_data["birth_year"]
    role = user_data["role"]
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO User(TCK, password, fullname, address, birth_year, role) VALUES (%s, %s, %s, %s, %s, %s)", (TCK,password, fullname, address, birth_year, role,))
    connection.commit()
    if role == "doctor":
        expertise_field = user_data["expertise_field"]
        hospital_id = user_data["hospital_id"]
        cursor.execute("INSERT INTO Doctor(TCK, expertise_field, hospital_id) VALUES (%s, %s, %s)", (TCK, expertise_field, hospital_id,))
        connection.commit()
    elif role == "patient":
        cursor.execute("INSERT INTO Patient(TCK) VALUES (%s)", (TCK,))
        connection.commit()
    elif role == "pharmaceuticalwarehouseworker":
        warehouse_id = user_data["warehouse_id"]
        cursor.execute("INSERT INTO PharmaceuticalWarehouseWorker(TCK, warehouse_id) VALUES (%s, %s)", (TCK, warehouse_id,))
        connection.commit()
    elif role == "pharmacist":
        pharmacy_id = user_data["pharmacy_id"]
        cursor.execute("INSERT INTO Pharmacist(TCK, pharmacy_id) VALUES (%s, %s)", (TCK, pharmacy_id,))
        connection.commit()
    return "successful"

@user.route('/delete/<int:TCK>', methods=['DELETE'])
def delete(TCK):

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT role FROM User WHERE TCK = %s", (TCK, ))
    role = cursor.fetchone()['role']


    if role.lower() == "doctor":
        cursor.execute("DELETE FROM Doctor WHERE TCK = %s", (TCK,))
        connection.commit()
    elif role.lower() == "patient":
        cursor.execute("DELETE FROM Patient WHERE TCK = %s", (TCK,))
        connection.commit()
    elif role.lower() == "pharmaceuticalwarehouseworker":
        cursor.execute("DELETE FROM PharmaceuticalWarehouseWorker WHERE TCK = %s", (TCK,))
        connection.commit()
    elif role.lower() == "pharmacist":
        cursor.execute("DELETE FROM Pharmacist WHERE TCK = %s", (TCK,))
        connection.commit()
    cursor.execute("DELETE FROM User WHERE TCK = %s", (TCK,))
    connection.commit()

    return 'success'

@user.route('/info', methods=['POST'])
def info():
    data = request.json
    TCK = data["TCK"]
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM User WHERE TCK = %s", (TCK, ))

    user_info = cursor.fetchone()
    role = user_info['role']
    if role == "pharmacist":
        cursor.execute("SELECT * FROM User NATURAL JOIN Pharmacist WHERE TCK = %s",(TCK,))
        return jsonify(cursor.fetchone())
    if role == "doctor":
        cursor.execute("SELECT * FROM User NATURAL JOIN Doctor WHERE TCK = %s",(TCK,))
        return jsonify(cursor.fetchone())
    if role == "pharmaceuticalwarehouseworker":
        cursor.execute("SELECT * FROM User NATURAL JOIN PharmaceuticalWarehouseWorker WHERE TCK = %s",(TCK,))
        return jsonify(cursor.fetchone())
    return jsonify(user_info)

@user.route('/login', methods = ['GET', 'POST'])
def login():
    data = request.json
    tck = data['TCK']
    password = data['password']

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM User WHERE TCK = %s AND password = %s", (tck, password))
    exist = cursor.fetchone()

    if exist:
        session['loggedin'] = True
        session['TCK'] = tck
        session['password'] = password
        return jsonify(exist)

    return "Your TCK or password is not valid. Try again"

@user.route('/logout', methods = ['GET', 'POST'])
def logout():
    session['TCK'] = None
    session['password'] = None
    session['loggedin'] = False

    return "Successfully logged out"


@user.route('/listOrders', methods = ['POST'])
def listOrders():
    data = request.json
    TCK = data["patient_TCK"]
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM OrdersView WHERE patient_TCK = %s ORDER BY order_date DESC", (TCK,))
    return jsonify(cursor.fetchall())


@user.route('/listPrescriptions', methods = ['POST'])
def listPreservative():
    data = request.json
    patient_TCK = data["patient_TCK"]
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT DISTINCT drug_name, presc_id, illness, fullname, expertise_field, date FROM Prescription NATURAL JOIN (SELECT * FROM Prescribes WHERE patient_TCK = %s) as temp NATURAL JOIN Contains NATURAL JOIN Drug JOIN (Doctor NATURAL JOIN User) ON doctor_TCK = TCK ORDER BY date ASC", (patient_TCK,))
    return jsonify(cursor.fetchall())

@user.route('/listPatients', methods = ['POST'])
def listPatient():
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT fullname, TCK FROM Patient NATURAL JOIN User")
    return jsonify(cursor.fetchall())

@user.route('/all', methods = ['GET', 'POST'])
def listAllUsers():
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * From User")
    return jsonify(cursor.fetchall())

