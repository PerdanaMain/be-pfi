from app import app, prefix
from flask import request
from app.controllers.master_equipment_controller import (
    index,
    create,
    show,
    update,
    delete,
)


@app.route(prefix + "/equipments", methods=["GET"])
def get_equipments():
    return index()


@app.route(prefix + "/equipments", methods=["POST"])
def create_equipment():
    return create()


@app.route(prefix + "/equipment/<uuid:id>", methods=["GET", "PUT", "DELETE"])
def detail_equipment(id):
    if request.method == "GET":
        return show(id)
    elif request.method == "PUT":
        return update(id)
    elif request.method == "DELETE":
        return delete(id)
