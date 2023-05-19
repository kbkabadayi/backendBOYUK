import re
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS
import datetime


app = Flask(__name__)
CORS(app)

app.secret_key = 'abcdefgh'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'pompa'

mysql = MySQL(app)


@app.route('/')

@app.route('/addUser', methods=['GET', 'POST'])
def add_user():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Drug")
    data = cursor.fetchall()
    return jsonify(data)
    



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


# Running app
if __name__ == '__main__':
    app.run(debug=True)