from app import app, prefix
from flask import request
from app.middlewares.token_verify import token_required
from app.controllers.admin_controller import (
    index,
    get_equipment_search,
)


@token_required
@app.route(prefix + "/admin/equipments", methods=["GET"])
def get_admin():
    return index()


@token_required
@app.route(prefix + "/admin/equipment/search", methods=["GET"])
def get_equipment_search_route():
    return get_equipment_search()
