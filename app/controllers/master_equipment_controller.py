from flask import jsonify, make_response
from app.resources.master_equipment_resource import equipment_resource
from digital_twin_migration.models.pfi_app import PFIEquipment, PFICategory


def index():
    try:
        data = []

        return make_response(
            jsonify(
                {
                    "status": True,
                    "message": "Master Equipments fetched successfully",
                    "data": data,
                }
            ),
            200,
        )
    except Exception as e:
        return make_response(jsonify({"error": f"Internal Server Error: {e}"}), 500)
