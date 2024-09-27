from flask import request
from app.services.response import success, bad_request, not_found
from app.services.files.read import read_json
from app.services.orm.master_tag import get_tag_values_by_date


def index():
    try:

        return success(True, "Master Tags retrieved successfully", None)
    except Exception as e:
        return bad_request(False, str(e), None)


def search():
    try:
        tags = request.args.get("tags")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if not tags or not start_date or not end_date:
            return not_found(False, "Tags, start_date and end_date are required", None)

        tag_ids = [int(tag) for tag in tags.split(",")]

        data = get_tag_values_by_date(tag_ids, start_date, end_date)

        return success(True, "Value Tags retrieved successfully", data)
    except Exception as e:
        return bad_request(False, str(e), None)
