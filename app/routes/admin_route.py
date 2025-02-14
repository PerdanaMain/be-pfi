from app import app, prefix
from flask import request
from app.middlewares.token_verify import token_required
from app.controllers.admin_controller import (
    index,
    search,
    show,
    update,
    delete,
)


@token_required
@app.route(prefix + "/admin/equipments", methods=["GET"])
def get_admin():
    return index()


@token_required
@app.route(prefix + "/admin/equipment/search", methods=["GET"])
def get_equipment_search_route():
    return search()


@token_required
@app.route(prefix + "/equipment/<uuid:id>", methods=["GET", "PUT", "DELETE"])
def detail_equipment(id):
    if request.method == "GET":
        return show(str(id))
    elif request.method == "PUT":
        return update(str(id))
    elif request.method == "DELETE":
        return delete(str(id))
