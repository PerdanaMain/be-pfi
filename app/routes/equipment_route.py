from app import app, prefix
from flask import request
from app.middlewares.token_verify import token_required
from app.controllers.master_equipment_controller import (
    index,
    get_predicted_fail,
    create,
    show,
    update,
    delete,
    params,
)


@token_required
@app.route(prefix + "/equipments", methods=["GET"])
def get_equipments():
    return index()


@token_required
@app.route(prefix + "/equipments/predicted-fail", methods=["GET"])
def get_predicted_fail_equipments():
    return get_predicted_fail()


@token_required
@app.route(prefix + "/equipment", methods=["GET"])
def get_equipment():
    return params()


@token_required
@app.route(prefix + "/equipments", methods=["POST"])
def create_equipment():
    return create()


@token_required
@app.route(prefix + "/equipment/<uuid:id>", methods=["GET", "PUT", "DELETE"])
def detail_equipment(id):
    if request.method == "GET":
        return show(str(id))
    elif request.method == "PUT":
        return update(str(id))
    elif request.method == "DELETE":
        return delete(str(id))
