from flask import request
from app.services.response import success, created, bad_request
from app.services.orm.master_equipment import (
    get_all_equipments,
    get_equipment_by_id,
    create_equipment,
    update_equipment,
    delete_equipment,
)


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


def show(id):
    try:
        data = get_equipment_by_id(id)

        return success(True, "Master Equipment fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def update(id):
    try:
        req = request.get_json()

        data = {
            "name": req.get("name"),
            "parent_id": req.get("parent_id", None),
            "description": req.get("description"),
            "category_id": req.get("category_id"),
        }
        data = {key: value for key, value in data.items() if value is not None}

        update_equipment(id, data)

        return success(
            True, "Master Equipment updated successfully", get_equipment_by_id(id)
        )
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def delete(id):
    try:
        delete_equipment(id)

        return success(True, "Master Equipment deleted successfully", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
