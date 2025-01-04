from flask import request
from app.services.response import success, bad_request
from app.services.orm.eq_tree import (
    get_all_trees,
    get_tree_by_id,
    create_tree,
    update_tree,
    delete_tree,
)


def index():
    try:
        data = get_all_trees()
        return success(True, "Equipment Trees fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def create():
    try:
        req = request.get_json()

        data = {
            "name": req.get("name"),
            "level_no": req.get("level_no"),
            "name": req.get("name"),
        }

        create_tree(data)

        return success(True, "Equipment trees created successfullty", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def show(id):
    try:
        data = get_tree_by_id(id)

        return success(True, "Equipment Tree fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def update(id):
    try:
        req = request.get_json()

        data = {
            "name": req.get("name"),
            "level_no": req.get("level_no"),
            "name": req.get("name"),
        }

        data = {key: value for key, value in data.items() if value is not None}

        check = get_tree_by_id(id)
        if not check:
            return bad_request(False, "Equipment Tree not found", None)

        update_tree(id, data)

        return success(True, "Equipment Tree updated successfully", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def delete(id):
    try:
        check = get_tree_by_id(id)
        if not check:
            return bad_request(False, "Equipment Tree not found", None)

        delete_tree(id)

        return success(True, "Equipment Tree deleted successfully", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
