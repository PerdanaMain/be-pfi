from flask import request, Response
from app.services.response import *
from app.services.models.tag_model import *
from app.services.models.feature_data_model import *
from app.services.models.predict_model import *
from app.services.models.part_model import *
import time
import json


def index():
    try:
        # requests
        equipment_id = request.args.get("equipment_id", default=1, type=str)
        features_id = request.args.get("features_id", default=1, type=str)

        data = []

        values = get_data_values(equipment_id, features_id)

        detail = get_detail(equipment_id)
        trip = detail["upper_threshold"] / 2 * 1.5 + detail["upper_threshold"]
        showValues = []
        for value in values["values"]:
            if value["value"] < trip:
                showValues.append(value)

        prediction = get_predict_values(equipment_id, features_id)

        data.append(showValues)
        data.append(prediction)

        return success(
            True,
            "Data Prediction fetched successfully",
            data,
        )
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def detail():
    try:
        # requests
        part = request.args.get("part_id", default=1, type=str)

        data = []
        detail = get_detail(part)
        data.append(detail)

        return success(
            True,
            "Data Detail prediction successfully",
            data,
        )
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
