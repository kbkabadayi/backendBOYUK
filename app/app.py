import os
from flask import Flask, render_template, request, redirect, url_for, session, json
from flask_cors import CORS

from pharmacist import pharmacist
from hospital import hospital
from bank import bank
from drug import drugg
from warehouse import warehouse

from extensions import mysql

app = Flask(__name__)
CORS(app)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'pompa'

mysql.init_app(app)


app.register_blueprint(pharmacist)
app.register_blueprint(doctor)
app.register_blueprint(bank)
app.register_blueprint(drugg)
app.register_blueprint(warehouse)

@app.route('/')
@app.route('/data', methods=['GET'])
def get_time():
    x = datetime.datetime.now()
    response = {'Name': "pompa",
                              "Age": "22",
                              "Date": x,
                              "programming": "sucks ass"}
    return response



# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(debug=True, host='0.0.0.0', port=port)


# Running app
if __name__ == '__main__':
    app.run()
