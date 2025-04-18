from app import app, prefix
from flask import request
from app.middlewares.token_verify import token_required
from app.controllers.admin_controller import index, search, show, update, delete, unit


@token_required
@app.route(prefix + "/admin/equipments", methods=["GET"])
def get_admin():
    return index()


@token_required
@app.route(prefix + "/admin/equipment/<uuid:id>", methods=["GET", "PUT"])
def get_admin_equipment(id):
    if request.method == "GET":
        return show(str(id))
    elif request.method == "PUT":
        return update(str(id))


@token_required
@app.route(prefix + "/admin/equipment/search", methods=["GET"])
def get_equipment_search_route():
    return search()


@token_required
@app.route(prefix + "/admin/units", methods=["GET"])
def get_unit_route():
    return unit()
