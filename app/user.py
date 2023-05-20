from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors


user = Blueprint('user', __name__, url_prefix='/user')

# @user.route('/add', methods=['GET','POST'])
# def add():

#     user_data = request.json
#     TCK = user_data["TCK"]
#     password = user_data["password"]
#     fullname = user_data["fullname"]
#     address = user_data["address"]
#     birth_year = user_data["birth_year"]
#     role = user_data["role"]
#     connection = get_connection()
#     cursor = connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("INSERT INTO User(TCK, password, fullname, address, birth_year, role) VALUES (%s, %s, %s, %s, %s, %s, %s)", (TCK,password, fullname, address, birth_year, role))
#     connection.commit()
#     if role == "doctor":
#         expertise_field = user_data["expertise_field"]
#         hospital_id = user_data["hospital_id"]
#         cursor.execute("INSERT INTO Doctor(TCK, expertise_field, hospital_id) VALUES (%s, %s, %s)", (TCK, expertise_field, hospital_id))
#         connection.commit()
#     elif role == "patient":
#         bank_account_no = user_data["bank_account_no"]
#         cursor.execute("INSERT INTO Patient(TCK, bank_account_no) VALUES (%s, %s, %s)", (TCK, bank_account_no))
#         connection.commit()
#     elif role ==



#     return hospital_data
