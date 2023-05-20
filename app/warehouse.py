from flask import Blueprint, jsonify, request
from database import get_connection
import MySQLdb.cursors

warehouse = Blueprint('warehouse', __name__, url_prefix='/warehouse')

