from flask import Flask
from flask_cors import CORS
import psycopg2
import configparser
from flask_restx import Api, Resource, fields

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='API for Database Operations',
          description='A simple API for inserting and managing database entries')

config = configparser.ConfigParser()
config.read('config_file/webconfig.ini')

ns = api.namespace('database', description='Database operations')

# Define the model for user input
user_model = api.model('User', {
    'name': fields.String(required=True, description='The user name'),
    'password': fields.String(required=True, description='The user password')
})

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

@ns.route('/insert')
class Insert(Resource):
    @ns.doc('insert_user')
    @ns.expect(user_model)  # Expecting the user model as input
    def post(self):
        """Inserts a new user into the database."""
        data = api.payload  # Get data from request
        connection = database_details()
        if isinstance(connection, str):  # If the connection is an error message string
            return connection, 500
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (name, password) VALUES (%s, %s)", (data['name'], data['password']))
            connection.commit()
            cursor.close()
            connection.close()
            return "Data inserted successfully", 200
        except psycopg2.Error as e:
            return f"Error inserting into table: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
