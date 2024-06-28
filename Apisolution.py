from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import configparser
app = Flask(__name__)
CORS(app)

@app.route('/Login')
def Login():
    
    
    #conn = connection.cursor()
    #conn.execute('select * from users1')
    #row = conn.fetchall()
    data = 'github'
    return jsonify(data)






if __name__ == '__main__':
    app.run(debug=True,port=5001)
