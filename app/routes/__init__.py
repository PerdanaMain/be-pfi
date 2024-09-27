from app import app, prefix
from flask import jsonify, make_response
from app.routes import tag_route, value_tag_route, equipment_route, category_route
from digital_twin_migration.database import db
from sqlalchemy import text
from app.services.response import not_found
from config import Config
from app.middlewares.token_verify import token_required


@app.before_request
@token_required
def before_request():
    pass


@app.route(prefix + "/")
def index():
    print(Config.SQLALCHEMY_DATABASE_URI)

    try:
        conn = db.engine.connect().execute(text("SELECT 1"))
        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Welcome to Digital Twin API",
                    "data": conn.scalar(),
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
