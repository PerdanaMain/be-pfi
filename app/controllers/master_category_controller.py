from flask import jsonify, make_response, request
from app.resources.master_category_resource import category_resource
from digital_twin_migration.models.pfi_app import PFICategory
from digital_twin_migration.database import Transactional, Propagation


def index():
    try:
        categories = PFICategory.query.all()

        data = []
        if len(categories) > 0:
            for ctg in categories:
                data.append(category_resource(ctg))
        else:
            data = None
        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Master Category fetched successfully",
                    "data": data,
                }
            ),
            200,
        )
    except Exception as e:
        return make_response(jsonify({"error": f"Internal Server Error: {e}"}), 500)


@Transactional(propagation=Propagation.REQUIRED)
def create():
    try:
        req = request.get_json()

        data = {
            "name": req.get("name"),
        }
        category = PFICategory(**data)
        category.save()
        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Master Category created successfully",
                    "data": None,
                }
            ),
            200,
        )
    except Exception as e:
        return make_response(jsonify({"error": f"Internal Server Error: {e}"}), 500)


@Transactional(propagation=Propagation.REQUIRED)
def delete(id):
    try:
        category = PFICategory.query.filter_by(id=id).first()
        if category is None:
            return make_response(
                jsonify(
                    {
                        "status": False,
                        "message": "Master Category not found",
                        "data": None,
                    }
                ),
                404,
            )

        category.delete()
        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Master Category deleted successfully",
                    "data": None,
                }
            ),
            200,
        )
    except Exception as e:
        return make_response(jsonify({"error": f"Internal Server Error: {e}"}), 500)
