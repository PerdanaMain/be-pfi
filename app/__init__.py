from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

# Define upload folder path inside public
UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

app = Flask(__name__, static_folder=STATIC_FOLDER)


# This should represent the path where files get saved during upload
app.config["UPLOAD_FOLDER"] = os.path.join(STATIC_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB limit

CORS(app)


@app.route("/static/uploads/equipments/<path:filename>")
def uploaded_file(filename):
    return send_from_directory("static/uploads/equipments/", filename)


prefix = "/api/v1"

from app import routes
from app import controllers
