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
from datetime import datetime
from app.config.database import get_connection


def test_connection():
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Eksekusi query sederhana untuk test koneksi
        cur.execute("SELECT 1")
        result = cur.fetchone()

        # Tutup cursor dan koneksi
        cur.close()
        conn.close()

        connection_info = {
            "database_connected": True,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "server_status": "running",
        }

        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Database connection successful",
                    "data": connection_info,
                }
            ),
            200,
        )

    except Exception as e:
        return make_response(
            jsonify(
                {
                    "status": False,
                    "message": f"Database connection failed: {str(e)}",
                    "data": None,
                }
            ),
            500,  # Gunakan 500 untuk error server
        )


@app.route(prefix + "/")
def index():

    try:
        api_info = test_connection().get_json()
        return make_response(api_info, 200)
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
