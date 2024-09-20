from flask import jsonify, make_response
from app.models.master_tag_model import MasterTag


def index():
    try:
        master_tags = MasterTag.query.all()

        master_tags_list = [
            {
                "id": tag.id,
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
                "tag_values": [
                    {
                        "id": value.id,
                        "time_stamp": value.time_stamp,
                        "value": value.value,
                        "units_abbreviation": value.units_abbreviation,
                        "good": value.good,
                        "questionable": value.questionable,
                        "substituted": value.substituted,
                        "annotated": value.annotated,
                    }
                    for value in tag.tag_values
                ],
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
