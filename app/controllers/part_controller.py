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

        part = get_part(str(id))

        if part is None:
            return not_found(False, "Part not found", None)

        if req["unit_id"] is None:
            return bad_request(False, "Unit ID is required", None)
        if req["unit_id"] == "":
            return bad_request(False, "Unit ID can't be empty", None)

        if req["part_name"] is None or req["part_name"] == "":
            return bad_request(False, "Part Name is required", None)
        if req["part_name"] == "":
            return bad_request(False, "Part name can't be empty", None)

        if req["location_tag"] is None or req["location_tag"] == "":
            return bad_request(False, "Part location tag is required", None)
        if req["location_tag"] == "":
            return bad_request(False, "Part location can't be empty", None)

        if req["alarm_threshold"] is None:
            return bad_request(False, "Alarm Threshold is required", None)
        if not isinstance(req["alarm_threshold"], (int, float)):
            return bad_request(False, "Alarm Threshold must be a number", None)

        if req["trip_threshold"] is None:
            return bad_request(False, "Trip Threshold is required", None)
        if not isinstance(req["trip_threshold"], (int, float)):
            return bad_request(False, "trip Threshold must be a number", None)

        if req["normal_value"] is None:
            return bad_request(False, "Normal Value is required", None)
        if not isinstance(req["normal_value"], (int, float)):
            return bad_request(False, "normal value must be a number", None)

        data = update_part(str(id), req)
        return success(True, "Master Equipment updated successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
