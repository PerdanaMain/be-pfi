from flask import jsonify, make_response
from sqlalchemy.orm import joinedload
from app.models.master_tag_model import MasterTag


def index():
    try:
        master_tags = MasterTag.query.all()

        master_tags_list = [
            {
                "tag_id": tag.id,
                "web_id": tag.web_id,
                "name": tag.name,
                "path": tag.path,
                "descriptor": tag.descriptor,
                "point_class": tag.point_class,
                "point_type": tag.point_type,
                "digital_set_name": tag.digital_set_name,
                "engineering_units": tag.engineering_units,
                "span": tag.span,
                "zero": tag.zero,
                "step": tag.step,
                "future": tag.future,
                "display_digits": tag.display_digits,
            }
            for tag in master_tags
        ]

        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Master Tags fetched successfully",
                    "data": master_tags_list,
                }
            ),
            200,
        )
    except Exception as e:
        return make_response(jsonify({"error": f"Internal Server Error: {e}"}), 500)
