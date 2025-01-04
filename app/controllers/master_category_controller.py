from flask import request
from app.services.response import success, created, bad_request
from app.services.orm.master_category import (
    get_all_categories,
    create_category,
    delete_category,
)


def index():
    try:
        data = get_all_categories()

        return success(True, "Master Categories fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def create():
    try:
        req = request.get_json()

        data = {
            "name": req.get("name"),
            "rigid_or_flexy": req.get("rigid_or_flexy"),
            "edges_a": req.get("edges_a"),
            "edges_b": req.get("edges_b"),
            "edges_c": req.get("edges_c"),
            "edges_d": req.get("edges_d"),
        }
        create_category(data)
        return created(True, "Master Category created successfully", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def delete(id):
    try:
        delete_category(id)
        return success(True, "Master Category deleted successfully", id)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
