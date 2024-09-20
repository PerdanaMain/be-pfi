from flask import jsonify, make_response, request
from app.models.value_tag_model import ValueTag
from datetime import datetime


def search():
    try:
        tags = request.args.get("tags")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if not tags or not start_date or not end_date:
            return make_response(jsonify({"error": "Missing parameters"}), 400)

        tag_ids = [int(tag) for tag in tags.split(",")]
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)

        if start_date == end_date:
            end_date = end_date.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )

        value_tags = ValueTag.query.filter(
            ValueTag.tag_id.in_(tag_ids),
            ValueTag.time_stamp >= start_date,
            ValueTag.time_stamp <= end_date,
        ).all()

        value_tags_list = [
            {
                "tag_id": tag.tag_id,
                "time_stamp": tag.time_stamp,
                "value": tag.value,
                "units_abbreviation": tag.units_abbreviation,
                "good": tag.good,
                "questionable": tag.questionable,
                "substituted": tag.substituted,
                "annotated": tag.annotated,
            }
            for tag in value_tags
        ]

        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Value Tags fetched successfully",
                    "data": value_tags_list,
                    "request": {
                        "tags": tags,
                        "start_date": start_date,
                        "end_date": end_date,
                    },
                }
            ),
            200,
        )
    except Exception as e:
        return make_response(jsonify({"error": f"Internal Server Error: {e}"}), 500)
