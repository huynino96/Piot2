from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from config import Config
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__, static_folder='static', static_url_path='/')  # Specify the static path
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)   # Use flask_cors to allow cross origin request
basic_auth = BasicAuth(app) # Use basic auth to protect our RESTapi end points
api = Api(app)  # Use flask_api to use convenient methods for creating rest api in flask

from app import routes, models