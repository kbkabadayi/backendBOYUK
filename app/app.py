import re
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS
from pharmacist import pharmacist
from hospital import hospital
from bank import bank
from drug import drug
from warehouse import warehouse
from flask_swagger_ui import get_swaggerui_blueprint
import datetime

app = Flask(__name__)
CORS(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.register_blueprint(pharmacist)
app.register_blueprint(hospital)
app.register_blueprint(bank)
app.register_blueprint(drug)
app.register_blueprint(warehouse)

app.secret_key = 'abcdefgh'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'pompa'

mysql = MySQL(app)


@app.route('/')
@app.route('/data', methods=['GET'])
def get_time():
    x = datetime.datetime.now()
    response = {'Name': "pompa",
                              "Age": "22",
                              "Date": x,
                              "programming": "sucks ass"}
    return response

@app.route('/addUser', methods=['GET', 'POST'])
def add_user():
    data = request.json
    return data["TCK"]

@app.route('/add_drug', methods = ['GET', 'POST'])
def add_drug():
    data = request.json
    drug_name = data['drug_name']
    needs_prescription = data['needs_prescription']
    drug_class = data['drug_class'] 
    side_effects = data['side_effects']
    
    
    return side_effects

@app.route('/add_pharmacy', methods = ['GET', 'POST'])
def add_pharmacy():
    data = request.json
    pharmacy_id = data['pharmacy_id']
    pharm_name = data['pharm_name']
    pharm_city = data['pharm_city']
    
    return pharmacy_id

@app.route('/add_hospital', methods = ['GET', 'POST'])
def add_hospital():
    data = request.json
    hospital_id = data['hospital_id']
    name = data['name']
    city = data['city']
    
    return city


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


# Running app
if __name__ == '__main__':
    app.run(debug=True)
