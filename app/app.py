import re
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import datetime
from database import db
from hospital import hospital
from pharmacy import pharmacy

#app = Flask(__name__)
CORS(db)

db.register_blueprint(hospital)
db.register_blueprint(pharmacy)

@db.route('/')
@db.route('/data', methods=['GET'])
def get_time():
    x = datetime.datetime.now()
    response = {'Name': "pompa",
                              "Age": "22",
                              "Date": x,
                              "programming": "sucks ass"}
    return response

@db.route('/addUser', methods=['GET', 'POST'])
def add_user():
    data = request.json
    return data["TCK"]

@db.route('/add_drug', methods = ['GET', 'POST'])
def add_drug():
    data = request.json
    drug_name = data['drug_name']
    needs_prescription = data['needs_prescription']
    drug_class = data['drug_class']
    side_effects = data['side_effects']


    return side_effects

@db.route('/add_pharmacy', methods = ['GET', 'POST'])
def add_pharmacy():
    data = request.json
    pharmacy_id = data['pharmacy_id']
    pharm_name = data['pharm_name']
    pharm_city = data['pharm_city']

    return pharmacy_id

@db.route('/add_hospital', methods = ['GET', 'POST'])
def add_hospital():
    data = request.json
    hospital_id = data['hospital_id']
    name = data['name']
    city = data['city']

    return city


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    db.run(debug=True, host='0.0.0.0', port=port)


# Running app
if __name__ == '__main__':
    db.run(debug=True)
