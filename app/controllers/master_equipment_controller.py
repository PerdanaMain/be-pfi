from flask import request
from app.services.orm.master_equipment import get_all_equipments, create_equipment
from app.services.response import success, created, bad_request


def index():
    try:
        data = get_all_equipments()

        return success(True, "Master Equipment fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def create():
    try:
        req = request.get_json()

        data = {
            "name": req.get("name"),
            "parent_id": req.get("parent_id") if req.get("parent_id") else None,
            "description": req.get("description"),
            "category_id": req.get("category_id"),
        }
        create_equipment(data)

        return created(True, "Master Equipment created successfully", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
