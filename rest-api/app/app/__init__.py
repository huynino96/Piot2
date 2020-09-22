from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_restful import Api
from flask_cors import CORS
import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "The Chosen One"
    # CloudSQL & SQLAlchemy configuration
    # Replace the following values the respective values of your Cloud SQL
    # instance.
    CLOUDSQL_USER = 'root'
    CLOUDSQL_PASSWORD = 'HJrMEtG2hB0FNqit'
    CLOUDSQL_DATABASE = 'car'
    # Set this value to the Cloud SQL connection name, e.g.
    #   "red-planet-288402:asia-southeast1:piot2".
    # You must also update the value in app.yaml.
    CLOUDSQL_CONNECTION_NAME = 'red-planet-288402:asia-southeast1:piot2'
    CLOUDSQL_CONNECTION_PORT = 3306

    # The CloudSQL proxy is used locally to connect to the cloudsql instance.
    # To start the proxy, use:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    # Port 3306 is the standard MySQL port. If you need to use a different port,
    # change the 3306 to a different port number.

    # Alternatively, you could use a local MySQL instance for testing.
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{user}:{password}@34.87.84.69:{port}/{database}').format(
        user=CLOUDSQL_USER,
        password=CLOUDSQL_PASSWORD,
        port=CLOUDSQL_CONNECTION_PORT,
        database=CLOUDSQL_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Basic auth parameter
    BASIC_AUTH_USERNAME = 'Rmit'
    BASIC_AUTH_PASSWORD = 'rmit'

    # CORS setting
    CORS_HEADERS = 'Content-Type'



app = Flask(__name__, static_folder='static', static_url_path='/')  # Specify the static path
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)   # Use flask_cors to allow cross origin request
basic_auth = BasicAuth(app) # Use basic auth to protect our RESTapi end points
api = Api(app)  # Use flask_api to use convenient methods for creating rest api in flask

from app import routes, models
