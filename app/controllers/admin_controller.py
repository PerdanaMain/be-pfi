from flask import request
from app.services.response import *
from app.services.models.equipment_model import *
from app.services.models.tag_model import *
from app.services.models.part_model import *
from app.services.models.eq_tree_model import *
from app.services.models.unit_model import *
from app.config.config import Config
from werkzeug.utils import secure_filename
import os


def index():
    try:
        # requests
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=10, type=int)

        tree = "53325b34-3f97-4f37-95cc-4a32b9de92de"
        data = get_equipments_for_admin(tree=tree, page=page, limit=limit)

        return success(True, "Master Equipment for admin fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def unit():
    try:
        data = get_units()
        return success(True, "Units fetched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def search():
    try:
        name = request.args.get("name", default="", type=str)

        data = search_equipment(name)
        for equipment in data:
            sub_system = get_parent_equipments(equipment["parent_id"])
            equipment["sub_system"] = sub_system
            system = get_parent_equipments(sub_system["parent_id"])
            equipment["system"] = system

        return success(True, "Equipment searched successfully", data)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def show(id):
    try:
        host = request.host_url

        equipment = get_equipment_for_admin(id)
        equipment = equipment["equipments"]
        sub_system = get_parent_equipments(equipment["parent_id"])
        equipment["sub_system"] = sub_system
        system = get_parent_equipments(sub_system["parent_id"])
        equipment["system"] = system

        # Construct the image URL - This assumes uploads is inside the public folder
        if equipment["image_name"]:
            # Remove trailing slash from host if present
            host = host.rstrip("/")
            equipment["image_url"] = (
                f"{host}/{Config.STATIC_FOLDER}/{equipment['image_name']}"
            )
        else:
            equipment["image_url"] = None

        return success(
            True, "Equipment fetched successfully", {"equipments": equipment}
        )
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def update(id):
    try:
        ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
        image_name = None
        assetnum = request.form.get("assetnum", default="", type=str)
        location_tag = request.form.get("location_tag", default="", type=str)
        system_tag = request.form.get("system_tag", default="", type=str)
        name = request.form.get("name", default="", type=str)

        equipment = get_equipment(id)

        if request.files:
            image = request.files["image"]

            # delete old image
            if equipment["equipments"]["image_name"]:
                os.remove(
                    os.path.join(
                        Config.UPLOAD_FOLDER, equipment["equipments"]["image_name"]
                    )
                )

            if image.filename == "":
                return not_found(False, "No image selected", None)

            if image and allowed_file(image.filename):
                ext = image.filename.rsplit(".", 1)[1].lower()
                image_name = f"{uuid.uuid4().hex}.{ext}"
                fpath = os.path.join(Config.UPLOAD_FOLDER, image_name)
                image.save(fpath)

            else:
                return bad_request(False, "Invalid image type", None)

        data = {
            "name": name,
            "assetnum": assetnum,
            "location_tag": location_tag,
            "system_tag": system_tag,
            "image_name": image_name,
        }
        update_equipment_for_admin(id=id, data=data)

        return success(True, "Equipment updated successfully", image_name)

    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def delete():
    try:
        id = request.args.get("id", default="", type=str)
    except Exception as e:
        return bad_request(False, f"Internal Server Error: {e}", None)


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    :param filename: Name of the uploaded file
    :return: Boolean indicating if the file is allowed
    """
    ALLOWED_EXTENSIONS = Config.ALLOWED_IMAGE_EXTENSIONS
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
