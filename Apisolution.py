from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import configparser
import logging
from flask_restx import Api, Resource, fields

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Login API',
          description='API for user login',
          )

logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def db_connection():
    config = configparser.ConfigParser()
    config.read('config/webconfig.ini')
    db_config = {
        "db_name": config.get('database', 'db_name'),
        "db_user": config.get('database', 'db_user'),
        "db_password": config.get('database', 'db_password'),
        "db_host": config.get('database', 'db_host'),
        "db_port": config.get('database', 'db_port')
    }
    connection_string = (
        f"dbname={db_config['db_name']} "
        f"user={db_config['db_user']} "
        f"password={db_config['db_password']} "
        f"host={db_config['db_host']} "
        f"port={db_config['db_port']}"
    )
    try:
        return psycopg2.connect(connection_string)
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return None

ns = api.namespace('Login', description='Login operations')

login_model = api.model('Login', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

@ns.route('/')
class Login(Resource):
    @ns.expect(login_model)
    @ns.response(200, 'Login successful')
    @ns.response(401, 'Invalid credentials')
    @ns.response(500, 'Database connection error')
    def post(self):
        """User login"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        conn = db_connection()
        if conn is None:
            return {'error': 'Database connection error'}, 500

        try:
            cursor = conn.cursor()
            query = 'SELECT * FROM users1 WHERE username = %s AND password = %s'
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                return {'message': 'Login successful'}
            else:
                return {'message': 'Invalid credentials'}, 401
        except Exception as e:
            logging.error(f"Error during login: {e}")
            return {'error': 'Error during login'}, 500
        finally:
            if conn:
                cursor.close()
                conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)

