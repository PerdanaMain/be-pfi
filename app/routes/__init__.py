from app import app, prefix
from flask import jsonify, make_response
from app.routes import (
    equipment_route,
    category_route,
    eq_tree_route,
    predict_route,
    feature_route,
)
from app.services.response import not_found
from app.config.database import get_connection


@app.route(prefix + "/")
def index():

    try:

        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Welcome to Digital Twin API",
                    "data": get_connection(),
                }
            ),
            200,
        )
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "status": False,
                    "message": "DB Connection Error : " + str(e),
                    "data": None,
                }
            ),
            200,
        )


@app.errorhandler(404)
def route_not_found(e):
    return not_found(False, f"Route not found, {e}", None)
