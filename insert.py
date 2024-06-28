from flask import Flask
import psycopg2
from flask_cors import CORS
import configparser
app = Flask(__name__)
CORS(app)
config = configparser.ConfigParser()
config.read('config/webconfig.ini')

@app.route('/insert')
def insert():
    
    
if __name__ == '__main__':
    app.run(debug = True)

