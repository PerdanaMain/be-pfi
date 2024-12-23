from flask import request
from app.services.response import *
from app.services.models.feature_data_model import get_last_data_value


def information_chart():
    try:
        features_id = request.args.get("features_id", default=1, type=str)
        part_id = request.args.get("part_id", default=1, type=str)

        informations = []
        current_value = get_last_data_value(part_id=part_id, feature_id=features_id)

        informations.append(
            {
                "name": "Predicted Time to Failure",
                "value": "> 3",
                "satuan": "Month",
            }
        )
        informations.append(
            {
                "name": "Current Condition",
                "value": 100,
                "satuan": "%",
            },
        )
        informations.append(
            {
                "name": "Current Value",
                "value": round(current_value, 4),
                "satuan": "um",
            },
        )
        informations.append(
            {
                "name": "Mean Time to Repair",
                "value": 100,
                "satuan": "hours",
            },
        )
        return success(True, "Chart Information Fetched Successfully", informations)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
