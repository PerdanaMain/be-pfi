from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()


UPLOAD_FOLDER = "uploads"

app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit


CORS(app)

prefix = "/api/v1"


from app import routes
from app import controllers
