from app.services.models.feature_model import *
from app.services.response import *


def index():
    try:
        data = get_features()

        return success(True, "Data Features fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error, {e}", None)


def show(id):
    try:

        if not id or id == "":
            return bad_request(False, "Id is required", None)

        data = get_feature(id)
        if data:
            return success(True, "Data Features fetched successfully", data)
        else:
            return not_found(False, "Data Features not found", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def store(data):
    try:
        name = data["name"]
        category = data["category"]

        if not name or name == "":
            return bad_request(False, "Name is required", None)

        if not category or category == "":
            return bad_request(False, "Category is required ", None)

        response = create_feature(name, category)
        return success(True, "Data Features stored successfully", response)
    except Exception as e:
        return bad_request(False, f"Internal Server Error, {e}", None)


def update(id, data):
    try:
        name = data["name"]
        category = data["category"]

        if not id or id == "":
            return bad_request(False, "Id is required", None)

        if not name or name == "":
            return bad_request(False, "Name is required", None)

        if not category or category == "":
            return bad_request(False, "Category is required ", None)

        response = update_feature(id, name, category)
        return success(True, "Data Features updated successfully", response)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def destroy(id):
    try:

        if not id or id == "":
            return bad_request(False, "Id is required", None)

        response = delete_feature(id)
        return success(True, "Data Features deleted successfully", response)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
