from flask import jsonify, make_response
from app import app, prefix
from app.controllers.master_tag_controller import index


@app.route(prefix + "/tags", methods=["GET"])
def get_tags():
    return index()
