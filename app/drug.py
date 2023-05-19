from flask import Blueprint, jsonify

drug = Blueprint('drug', __name__, url_prefix='/drug')

@drug.route('/endpoint4')
def endpoint2():
    return jsonify({'message': 'Endpoint 4'})