from flask import Flask
from config import Config
from flask_cors import CORS
from digital_twin_migration.database import db
from dotenv import load_dotenv

config = Config()
load_dotenv()


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config.from_object(Config)
db.init_app(app)

prefix = "/api/v1"


from app import routes
from app import controllers
