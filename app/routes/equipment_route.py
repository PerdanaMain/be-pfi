from app import app, prefix
from flask import request
from app.middlewares.token_verify import token_required
from app.controllers.master_equipment_controller import (
    index,
    create,
    show,
    update,
    delete,
    search,
    tag_index,
)


@token_required
@app.route(prefix + "/equipments", methods=["GET"])
def get_equipments():
    return index()


@token_required
@app.route(prefix + "/selected-tags", methods=["GET"])
def get_selected_tags():
    return tag_index()


@token_required
@app.route(prefix + "/equipments", methods=["POST"])
def create_equipment():
    return create()


@token_required
@app.route(prefix + "/equipment", methods=["GET"])
def get_equipment():
    return search()


@token_required
@app.route(prefix + "/equipment/<uuid:id>", methods=["GET", "PUT", "DELETE"])
def detail_equipment(id):
    if request.method == "GET":
        return show(id)
    elif request.method == "PUT":
        return update(id)
    elif request.method == "DELETE":
        return delete(id)
