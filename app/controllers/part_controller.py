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


def update(id):
    try:
        req = request.get_json()

        if req["unit_id"] is None:
            return bad_request(False, "Unit ID is required", None)
        if req["alarm_threshold"] is None:
            return bad_request(False, "Alarm Threshold is required", None)
        if req["trip_threshold"] is None:
            return bad_request(False, "Trip Threshold is required", None)
        if req["normal_value"] is None:
            return bad_request(False, "Normal Value is required", None)

        data = update_part(id, req)
        return success(True, "Master Equipment updated successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
