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
        # requests
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)

        data = get_all_equipments(page=page, limit=limit)

        return success(True, "Master Equipment fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def create():
    try:
        req = request.get_json()

        data = {
            "name": req.get("name"),
            "parent_id": req.get("parent_id") if req.get("parent_id") else None,
            "category_id": req.get("category_id"),
            "equipment_tree_id": req.get("equipment_tree_id"),
            "system_tag": req.get("system_tag"),
            "location_tag": req.get("location_tag"),
            "assetnum": req.get("assetnum"),
        }
        create_equipment(data)

        return created(True, "Master Equipment created successfully", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def show(id):
    try:
        # requests
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)

        data = get_equipment_by_id(id, page=page, limit=limit)

        return success(True, "Master Equipment fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def update(id):
    try:
        req = request.get_json()

        data = {
            "name": req.get("name"),
            "parent_id": req.get("parent_id") if req.get("parent_id") else None,
            "category_id": req.get("category_id"),
            "equipment_tree_id": req.get("equipment_tree_id"),
            "system_tag": req.get("system_tag"),
            "location_tag": req.get("location_tag"),
            "assetnum": req.get("assetnum"),
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
        equipment = get_equipment_by_id(id)

        if not equipment:
            return bad_request(False, "Master Equipment not found", None)

        delete_equipment(id)

        return success(True, "Master Equipment deleted successfully", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
