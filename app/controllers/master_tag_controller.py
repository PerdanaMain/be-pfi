from flask import jsonify, make_response
from app.models.master_tag_model import MasterTag
from app.resources.master_tag_resource import tag_resource


def index():
    try:
        master_tags = MasterTag.query.all()
        data = tag_resource(master_tags, relation=False)
        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Master Tags fetched successfully",
                    "data": data,
                }
            ),
            200,
        )
    except Exception as e:
        return make_response(jsonify({"error": f"Internal Server Error: {e}"}), 500)
