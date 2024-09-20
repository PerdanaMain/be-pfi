from app import app, prefix
from flask import jsonify, make_response
from app.routes import tag_route


@app.route(prefix + "/")
def index():
    return make_response(jsonify({"message": "Hello, World!"}), 200)
