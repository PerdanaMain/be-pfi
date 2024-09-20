from flask import jsonify, make_response, request
from app.models.value_tag_model import ValueTag
from app.models.master_tag_model import MasterTag
from app.resources.master_tag_resource import tag_resource
from datetime import datetime
from app import db


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

        query = (
            db.session.query(MasterTag).join(ValueTag).filter(MasterTag.id.in_(tag_ids))
        )

        if start_date == end_date:
            end_date = end_date.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )

        query = query.filter(
            ValueTag.time_stamp >= start_date,
            ValueTag.time_stamp <= end_date,
        )

        tags = query.all()

        data = tag_resource(tags, relation=True)

        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Value Tags fetched successfully",
                    "data": data,
                }
            ),
            200,
        )
    except Exception as e:
        return make_response(jsonify({"error": f"Internal Server Error: {e}"}), 500)
