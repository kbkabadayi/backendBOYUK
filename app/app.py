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
app.register_blueprint(doctor)
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



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


# Running app
if __name__ == '__main__':
    app.run(debug=True)
