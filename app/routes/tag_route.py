from flask import jsonify, make_response
from app import app

prefix = "/api/v1"


@app.route(prefix + "/tags", methods=["GET"])
def get_tags():
    return make_response(jsonify({"message": "GET tags", "data": []}), 200)
