from flask import Flask
import psycopg2
from flask_cors import CORS
app = Flask(__name__)
@app.route('/insert')
def insert():
    pass
if __name__ == '__main__':
    app.run(debug = True)

