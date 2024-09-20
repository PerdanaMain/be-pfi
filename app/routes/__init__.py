from app import app
from flask import jsonify, make_response
from app.routes import tag_route

prefix = "/api/v1"


@app.route(prefix + "/")
def index():
    return make_response(jsonify({"message": "Hello, World!"}), 200)
