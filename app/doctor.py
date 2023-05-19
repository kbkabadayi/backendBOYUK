from flask import Blueprint, jsonify

doctor = Blueprint('doctor', __name__, url_prefix='/doctor')

@hospital.route('/endpoint2')
def endpoint2():
    return jsonify({'message': 'Endpoint 2'})