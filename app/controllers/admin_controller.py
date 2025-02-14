from flask import request
from app.services.response import *
from app.services.models.equipment_model import *
from app.services.models.tag_model import *
from app.services.models.part_model import *
from app.services.models.eq_tree_model import *


def index():
    try:
        # requests
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)

        tree = "53325b34-3f97-4f37-95cc-4a32b9de92de"
        data = get_equipments_for_admin(tree=tree, page=page, limit=limit)

        for equipment in data["equipments"]:
            sub_system = get_parent_equipments(equipment["parent_id"])
            equipment["sub_system"] = sub_system
            system = get_parent_equipments(sub_system["parent_id"])
            equipment["system"] = system

        return success(True, "Master Equipment for admin fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def search():
    try:
        name = request.args.get("name", default="", type=str)

        data = search_equipment(name)
        for equipment in data:
            sub_system = get_parent_equipments(equipment["parent_id"])
            equipment["sub_system"] = sub_system
            system = get_parent_equipments(sub_system["parent_id"])
            equipment["system"] = system

        return success(True, "Equipment searched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def show():
    try:
        id = request.args.get("id", default="", type=str)

    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def update():
    try:
        id = request.args.get("id", default="", type=str)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def delete():
    try:
        id = request.args.get("id", default="", type=str)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
