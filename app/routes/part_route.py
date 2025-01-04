from app import app, prefix
from flask import request
from app.middlewares.token_verify import token_required
from app.controllers.part_controller import *


@app.route(prefix + "/part/<uuid:id>", methods=["GET"])
@token_required
def detail_part(id):
    return show(str(id))
