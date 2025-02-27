from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
CORS(app)

prefix = "/api/v1"


from app import routes
from app import controllers
