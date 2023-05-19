from flask import Blueprint, jsonify

warehouse = Blueprint('warehouse', __name__, url_prefix='/warehouse')

@warehouse.route('/endpoint5')
def endpoint2():
    return jsonify({'message': 'Endpoint 5'})