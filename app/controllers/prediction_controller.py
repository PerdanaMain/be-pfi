from flask import request
from app.services.response import *
from app.services.models.tag_model import get_tag_values


def index():
    try:
        # requests
        tag_id = request.args.get("tag_id", default=1, type=int)

        data = get_tag_values(tag_id)

        return success(True, "Data Prediction fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
