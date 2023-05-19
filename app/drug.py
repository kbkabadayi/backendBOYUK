from flask import Blueprint, jsonify
from extensions import mysql

drug = Blueprint('drugg', __name__, url_prefix='/drug')
con = mysql.connect()
cursor = con.cursor()

@drug.route('/add_drug', method = ['GET', 'POST'])
def add_drug():
    # data = request.json
    # drug_id = data['drug_id']
    # name = data['name']
    # needs_prescription = data['needs_prescription']
    # drug_class = data['drug_class']
    # drug_type = data['drug_type']
    
    
    cursor.execute('SELECT * FROM Drug')
    user = cursor.fetchone()
    
    return user