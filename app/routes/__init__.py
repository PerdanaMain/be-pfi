from app import app, prefix
from flask import jsonify, make_response
from app.routes import tag_route
from app.routes import value_tag_route
from app.routes import equipment_route
from app.routes import category_route
from digital_twin_migration.database import db
from sqlalchemy import text


@app.route(prefix + "/")
def index():

    try:
        db.engine.connect().execute(text("SELECT 1"))
        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Welcome to Digital Twin API",
                    "data": None,
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
