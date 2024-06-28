from flask import Flask
import psycopg2
from flask_cors import CORS
import configparser

app = Flask(__name__)
CORS(app)

config = configparser.ConfigParser()
config.read('config_file/webconfig.ini')

def database_details():
    try:
        db_name = config.get('database', 'db_name')
        db_user = config.get('database', 'db_user')
        db_password = config.get('database', 'db_password')
        db_host = config.get('database', 'db_host')
        db_port = config.get('database', 'db_port')
        
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        return conn  
    except psycopg2.Error as e:
        return f"Error connecting to database: {e}"

@app.route('/insert')
def insert():
    connection = database_details()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (name, password) VALUES ('loki', 'admin123')")
            connection.commit()
            cursor.close()
            connection.close()
            return "Data inserted successfully"
        except psycopg2.Error as e:
            return f"Error inserting into table: {e}"
    else:
        return "Failed to connect to database"

if __name__ == '__main__':
    app.run(debug=True)
