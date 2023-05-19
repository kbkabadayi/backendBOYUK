from flask import Blueprint, jsonify

hospital = Blueprint('hospital', __name__, url_prefix='/hospital')

@hospital.route('/endpoint2')
def endpoint2():
    return jsonify({'message': 'Endpoint 2'})