from flask import Blueprint, jsonify

bank = Blueprint('bank', __name__, url_prefix='/bank')

@bank.route('/endpoint3')
def endpoint2():
    return jsonify({'message': 'Endpoint 3'})