from flask import request
from app.services.response import *
from app.services.models.equipment_model import *
from app.services.models.tag_model import *
from app.services.models.part_model import *
from app.services.models.eq_tree_model import *


def index():
    try:
        # requests
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)

        data = get_equipments()

        return success(True, "Master Equipment fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def params():
    try:
        level = request.args.get("level", default=1, type=int)
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)

        eq_lvl = get_eq_tree_by_level(level)

        data = get_equipments_by_tree_id(eq_lvl["id"], page=page, limit=limit)

        return success(True, "Equipment Tree fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def get_systems_status():
    try:
        data = get_systems()

        return success(True, "Systems fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def report_equipments():
    try:
        parts = get_report_parts()

        return success(True, "Report fetched successfully", parts)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def filtered_report_equipments():
    try:
        equipment_id = request.args.get("equipment_id", type=str)
        unit_id = request.args.get("unit_id", type=str)
        sensor_type = request.args.get("sensorType", type=str)

        # Check if required parameters are present
        if not equipment_id and not unit_id and not sensor_type:
            return bad_request(False, "Missing required parameters", None)

        if equipment_id == "all":
            equipment_id = None
        if unit_id == "all":
            unit_id = None
        if sensor_type == "all":
            sensor_type = None

        parts = get_filtered_report_parts(equipment_id, unit_id, sensor_type)

        return success(
            True,
            "Report fetched successfully",
            {
                "parts": parts,
                "equipment_id": equipment_id,
                "unit_id": unit_id,
                "sensor_type": sensor_type,
            },
        )
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def create():
    try:
        req = request.get_json()

        name = req.get("name")
        parent_id = req.get("parent_id") if req.get("parent_id") else None
        category_id = req.get("category_id")
        equipment_tree_id = req.get("equipment_tree_id")
        system_tag = req.get("system_tag")
        location_tag = req.get("location_tag")
        assetnum = req.get("assetnum")

        if not name:
            return bad_request(False, "Name is required", None)
        if not category_id:
            return bad_request(False, "Category ID is required", None)
        if not equipment_tree_id:
            return bad_request(False, "Equipment Tree ID is required", None)

        create_equipment(
            name,
            equipment_tree_id,
            category_id,
            parent_id,
            assetnum,
            location_tag,
            system_tag,
        )

        return created(True, "Master Equipment created successfully", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def show(id):
    try:
        data = get_equipment(str(id))

        return success(True, "Master Equipment fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def update(id):
    try:
        req = request.get_json()

        data = {
            "name": req.get("name"),
            "parent_id": req.get("parent_id") if req.get("parent_id") else None,
            "category_id": req.get("category_id"),
            "equipment_tree_id": req.get("equipment_tree_id"),
            "system_tag": req.get("system_tag"),
            "location_tag": req.get("location_tag"),
            "assetnum": req.get("assetnum"),
        }
        data = {key: value for key, value in data.items() if value is not None}

        update_equipment(str(id), data)

        return success(True, "Master Equipment updated successfully", get_equipment(id))
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def delete(id):
    try:
        delete_equipment(id)

        return success(True, "Master Equipment deleted successfully", None)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)
