from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors
from datetime import datetime


drug = Blueprint('drug', __name__, url_prefix='/drug')

@drug.route('/registerDrug', methods=['POST'])
def registerDrug():
    data = request.json
    name = data["name"]
    needs_prescription = data["needs_prescription"]
    drug_class = data["drug_class"]
    drug_type = data["drug_type"]
    price = data["price"]

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO Drug VALUES (%s, %s, %s, %s, %s)", (name, needs_prescription, drug_class, drug_type, price))

    connection.commit()
    return jsonify({"result": "Drug added"})


@drug.route('/restockDrug', methods=['POST'])
def restockDrug():
    data = request.json
    drug_to_count = data["drug_to_count"]
    pharm_id = data["pharm_id"]
    warehouse_id = data["warehouse_id"]
    restock_date = datetime.now()

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    for drug_name, count in drug_to_count.items():
        cursor.execute("UPDATE HasDrug SET drug_count = drug_count + %s WHERE drug_name = %s AND pharmacy_id = %s", (count, drug_name, pharm_id))
        connection.commit()
        cursor.execute("INSERT INTO Restocks VALUES (%s, %s, %s, %s, %s)", (pharm_id, warehouse_id, drug_name, count, restock_date))
        connection.commit()

    return jsonify({"result": "Drug restocked to the pharmacy"})

@drug.route('/orderDrug', methods=['POST'])
def orderDrug():
    data = request.json
    patient_TCK = data["patient_TCK"]
    order_date = datetime.now()

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT pharm_id FROM Cart WHERE TCK = %s", (patient_TCK,))
    pharm_id = cursor.fetchone()['pharm_id']

    cursor.execute("SELECT drug_name, drug_count FROM Cart WHERE TCK = %s", (patient_TCK,))
    drug_to_count = cursor.fetchall()



    totalPrice = 0
    # check preconditions
    for i in range(len(drug_to_count)):
        drug_name = drug_to_count[i]['drug_name']
        count = drug_to_count[i]['drug_count']

        cursor.execute("SELECT price FROM Drug where name = %s", (drug_name,))
        price = cursor.fetchone()['price']

        totalPrice += price * count

        cursor.execute("SELECT drug_count FROM HasDrug WHERE pharmacy_id = %s AND drug_name = %s", (pharm_id, drug_name))
        count_in_pharm = cursor.fetchone()['drug_count']

        if (count > count_in_pharm):
            result_text = "Not enough " + drug_name + " in pharmacy"
            return jsonify({"status": "fail", "result": result_text})

        cursor.execute("SELECT needs_prescription FROM Drug WHERE name = %s", (drug_name,))
        requires = cursor.fetchone()['needs_prescription']
        if requires.lower() == 'yes':
            cursor.execute("SELECT drug_name FROM Contains WHERE presc_id in (SELECT presc_id FROM Prescribes WHERE patient_TCK = %s)", (patient_TCK,))
            drugs_prescribed = cursor.fetchall()
            pompa = {"drug_name": drug_name}

            if pompa not in drugs_prescribed:
                return jsonify({"status": "fail", "result": "Order contains a drug patient is not prescribed"})


    # process order
    for i in range(len(drug_to_count)):
        drug_name = drug_to_count[i]['drug_name']
        count = drug_to_count[i]['drug_count']

        cursor.execute("UPDATE HasDrug SET drug_count = drug_count - %s WHERE drug_name = %s AND pharmacy_id = %s", (count, drug_name, pharm_id))
        connection.commit()

        cursor.execute('SELECT bank_account_no FROM BankAccount WHERE patient_TCK = %s AND active = "active"', (patient_TCK,))
        bank_account_no = cursor.fetchone()['bank_account_no']

        status = "pompa"
        cursor.execute("INSERT INTO Orders VALUES (%s, %s, %s, %s, %s, %s)", (bank_account_no, patient_TCK, drug_name, order_date, count, status))
        connection.commit()

        cursor.execute("DELETE FROM Cart WHERE TCK = %s AND pharm_id = %s", (patient_TCK, pharm_id))
        connection.commit()


    cursor.execute("UPDATE BankAccount SET balance = balance - %s WHERE bank_account_no = %s", (totalPrice, bank_account_no))
    connection.commit()
    return jsonify({"status": "success", "result": "Drug ordered from"})

@drug.route('/filter', methods = ['POST'])
def filter():
    data = request.json
    min_price = data['min_price']
    max_price = data['max_price']
    # side_effect = data['side_effect']
    company = data['company']
    drug_type = data['drug_type']
    needs_prescription = data['needs_prescription']

    resulting_query = "SELECT * FROM Drug NATURAL JOIN HasDrug "
    where_clause = []

    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    if min_price:
        where_clause.append(f" price >= {min_price} ")

    if max_price:
        where_clause.append(f" price <= {max_price} ")

    # if side_effect:
    #     if len(side_effect) > 0:
    #         for i in range(len(side_effect)):
    #             where_clause.append(f" effect_name = {side_effect[i]} ")

    if needs_prescription == "0":
        needs = "no"
        where_clause.append(f" needs_prescription = '{needs}' ")


    if needs_prescription == "1":
        needs = "yes"
        where_clause.append(f" needs_prescription = '{needs}' ")

    if company:
        if len(company) > 0:
            side_query = "( "
            for i in range(len(company) - 1):
                side_query += f" company = '{company[i]}' OR "
            side_query += f" company = '{company[len(company) - 1]}' ) "
            where_clause.append( side_query)
    if drug_type != "all":
        where_clause.append(f" drug_type = '{drug_type}'")

    if len(where_clause) > 0:
        resulting_query += " WHERE "
        for i in range(len(where_clause) - 1):
            resulting_query += where_clause[i] + " AND "
        resulting_query += where_clause[len(where_clause) - 1]

    cursor.execute(resulting_query)
    result = cursor.fetchall()
    json_data = jsonify(result)


    return json_data


# Burayı şimdilik onur için ekliyoz sonra silcez
@drug.route('/list', methods = ['GET'])
def getAll():
    connection = get_connection()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM Drug")
    data = cursor.fetchall()

    return jsonify(data)







