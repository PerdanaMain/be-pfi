from flask import request
from app.services.response import *
from app.services.models.part_model import *


def index():
    try:
        data = get_all_parts()
        return success(True, "Master Equipment fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def show(id):
    try:
        data = get_part(str(id))

        if data is None:
            return not_found(False, "Part not found", None)

        return success(True, "Master Equipment fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
