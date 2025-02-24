from flask import request
from app.services.response import *
from app.services.models.oh_schedule_model import get_oh_schedule_by_year
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

def calculate_time_difference_to_hours(time_failure_str, date_time_str):
    if isinstance(time_failure_str, datetime) and isinstance(date_time_str, datetime):
        time_failure = time_failure_str
        date_time = date_time_str
    else:
        time_failure = datetime.strptime(time_failure_str, "%a, %d %b %Y %H:%M:%S GMT")
        date_time = datetime.strptime(date_time_str, "%a, %d %b %Y %H:%M:%S GMT")

    time_diff = time_failure - date_time
    hours_diff = time_diff.total_seconds() / 3600
    hours_diff = round(hours_diff)

    return hours_diff


def information_chart():
    try:
        features_id = request.args.get("features_id", default=1, type=str)
        part_id = request.args.get("part_id", default=1, type=str)

        informations = []
        current_value = get_last_data_value(part_id=part_id, feature_id=features_id)
        part = get_part(part_id)
        now = datetime.now()

        predict_time_to_failure = (
            calculate_time_difference(
                current_value["values"][0]["time_failure"],
                current_value["values"][0]["date_time"],
            )
            if current_value["values"][0]["predict_status"] == "predicted failed"
            else None
        )
        
        failure_hours = calculate_time_difference_to_hours(
            current_value["values"][0]["time_failure"],
            current_value["values"][0]["date_time"],
        ) if current_value["values"][0]["predict_status"] == "predicted failed" else None

        oh_schedules = get_oh_schedule_by_year(year=datetime.now().year)
        oh_start = calculate_time_difference(
            oh_schedules["oh_schedules"]["start"],
            now,
        )
        oh_start_hours = calculate_time_difference_to_hours(
            oh_schedules["oh_schedules"]["start"],
            now,
        )

        informations.append(
            {
                "name": f"predicted failure interval",
                "value": (
                    predict_time_to_failure
                    if predict_time_to_failure is not None
                    else oh_start
                ),
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
                "satuan": part["part"]["unit"],
            },
        )
        informations.append(
            {
                "name": "failure hours",
                "value": failure_hours if failure_hours is not None else oh_start_hours,
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
