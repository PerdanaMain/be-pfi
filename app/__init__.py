from flask import Flask
from config import Config
from flask_cors import CORS
from digital_twin_migration.database import db

config = Config()


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)
prefix = "/api/v1"


from app import routes
from app import models
from app import controllers
