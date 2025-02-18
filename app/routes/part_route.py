from app import app, prefix
from flask import request
from app.middlewares.token_verify import token_required
from app.controllers.part_controller import *


@app.route(prefix + "/parts", methods=["GET"])
# @token_required
def all_parts():
    return index()


@app.route(prefix + "/part/<uuid:id>", methods=["GET", "PUT"])
# @token_required
def detail_part(id):
    if request.method == "GET":
        return show(str(id))
    elif request.method == "PUT":
        return update(str(id))
