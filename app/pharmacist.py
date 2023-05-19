from flask import Blueprint, jsonify
from app import db  

pharmacist = Blueprint('pharmacist', __name__, url_prefix='/pharmacist')

@pharmacist.route('/endpoint1')
def endpoint2():
    return jsonify({'message': 'Endpoint 1'})