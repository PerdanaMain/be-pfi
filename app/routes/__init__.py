from app import app, prefix
from flask import jsonify, make_response
from app.routes import tag_route
from app.routes import value_tag_route


@app.route(prefix + "/")
def index():
    return make_response(
        jsonify(
            {
                "status": True,
                "message": "Welcome to the API",
                "data": None,
            }
        ),
        200,
    )
