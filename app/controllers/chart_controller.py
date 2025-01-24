from flask import request
from app.services.response import *
from app.services.models.feature_data_model import get_last_data_value
from app.services.models.part_model import get_part
from datetime import datetime
import requests


def calculate_time_difference(time_failure_str, date_time_str):
    if isinstance(time_failure_str, datetime) and isinstance(date_time_str, datetime):
        time_failure = time_failure_str
        date_time = date_time_str
    else:
        time_failure = datetime.strptime(time_failure_str, "%a, %d %b %Y %H:%M:%S GMT")
        date_time = datetime.strptime(date_time_str, "%a, %d %b %Y %H:%M:%S GMT")

    time_diff = time_failure - date_time
    days_diff = time_diff.total_seconds() / (24 * 3600)
    days_diff = round(days_diff)

    return days_diff


def information_chart():
    try:
        features_id = request.args.get("features_id", default=1, type=str)
        part_id = request.args.get("part_id", default=1, type=str)

        informations = []
        current_value = get_last_data_value(part_id=part_id, feature_id=features_id)
        part = get_part(part_id)
        location_tag = part["part"]["location_tag"]

        res = requests.get(
            f"http://192.168.1.82:8000/reliability/asset/mttr/{location_tag}"
        )
        res = res.json()

        mttr = "-"

        try:
            if res.get("data") and res["data"].get("hours") is not None:
                mttr = res["data"]["hours"]
        except (KeyError, AttributeError):
            mttr = "-"

        predict_time_to_failure = (
            calculate_time_difference(
                current_value["values"][0]["time_failure"],
                current_value["values"][0]["date_time"],
            )
            if current_value["values"][0]["predict_status"] == "predicted failed"
            else None
        )

        informations.append(
            {
                "name": f"predicted failure interval",
                "value": predict_time_to_failure if predict_time_to_failure else "-",
                "satuan": "Days",
            }
        )
        informations.append(
            {
                "name": "current condition",
                "value": "-",
                "satuan": "%",
            },
        )
        informations.append(
            {
                "name": "current value",
                "value": round(current_value["values"][0]["value"], 4),
                "satuan": "um",
            },
        )
        informations.append(
            {
                "name": "mean time to repair",
                "value": mttr,
                "satuan": "hours",
            },
        )
        return success(
            True,
            "Chart Information Fetched Successfully",
            informations,
        )
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
