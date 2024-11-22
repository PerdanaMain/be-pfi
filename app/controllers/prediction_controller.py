from flask import request, Response
from app.services.response import *
from app.services.models.tag_model import (
    get_predicted_values,
    get_tag_by_id,
    get_tag_values,
)
import time
import json


def index():
    try:
        # requests
        tag_id = request.args.get("tag_id", default=1, type=int)

        data = get_tag_values(tag_id)

        return success(True, "Data Prediction fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def stream_tag_value(tag_id, size, sleep):
    """
    Fungsi generator untuk streaming data dari database.
    """
    try:
        # Ambil data dari database
        data = get_tag_values(tag_id)

        batch_size = size
        total_data = len(data)

        for start in range(0, total_data, batch_size):
            # Ambil data dalam ukuran batch
            batch = data[start : start + batch_size]
            payload = {
                "data": batch,
                "size": size,
                "progress": f"{start + len(batch)} / {total_data}",
                "percentage": (start + len(batch)) / total_data * 100,
            }
            yield f"data: {json.dumps(payload)}\n\n"
            time.sleep(sleep)
    except Exception as e:
        # Tangani error
        error_data = {"error": str(e)}
        yield f"data: {json.dumps(error_data)}\n\n"


def stream_tag_prediction_value(tag_id, size, sleep):
    """
    Fungsi generator untuk streaming data dari database.
    """
    try:
        # Ambil data dari database
        data = get_tag_values(tag_id)

        batch_size = size
        total_data = len(data)

        for start in range(0, total_data, batch_size):
            # Ambil data dalam ukuran batch
            batch = data[start : start + batch_size]
            payload = {
                "data": batch,
                "size": size,
                "progress": f"{start + len(batch)} / {total_data}",
                "percentage": (start + len(batch)) / total_data * 100,
            }
            yield f"data: {json.dumps(payload)}\n\n"
            time.sleep(sleep)
    except Exception as e:
        # Tangani error
        error_data = {"error": str(e)}
        yield f"data: {json.dumps(error_data)}\n\n"
