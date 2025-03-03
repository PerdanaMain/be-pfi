from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

# Define upload folder path inside public
UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "public/uploads"

app = Flask(__name__, static_folder=STATIC_FOLDER)

# Create uploads directory inside the public folder
os.makedirs(os.path.join(STATIC_FOLDER, UPLOAD_FOLDER), exist_ok=True)

# This should represent the path where files get saved during upload
app.config["UPLOAD_FOLDER"] = os.path.join(STATIC_FOLDER, UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit

CORS(app)


@app.route("/public/uploads/equipment/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


prefix = "/api/v1"

from app import routes
from app import controllers
