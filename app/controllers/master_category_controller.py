from flask import jsonify, make_response, request
from app.resources.master_category_resource import category_resource
from digital_twin_migration.models.pfi_app import PFICategory
from digital_twin_migration.database import Transactional, Propagation
from app.services.response import success, created, bad_request, not_found
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


@Transactional(propagation=Propagation.REQUIRED)
def create():
    try:
        req = request.get_json()

        data = {
            "name": req.get("name"),
        }
        create_category(data)
        return created(True, "Master Category created successfully", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


@Transactional(propagation=Propagation.REQUIRED)
def delete(id):
    try:
        delete_category(id)
        return success(True, "Master Category deleted successfully", id)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
