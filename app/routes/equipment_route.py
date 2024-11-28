from app import app, prefix
from flask import request
from app.middlewares.token_verify import token_required
from app.controllers.master_equipment_controller import (
    index,
    create,
    show,
    update,
    delete,
    params,
    selected_tag,
    tag_index,
    tag_psd_values,
    tag_by_id,
)


@token_required
@app.route(prefix + "/equipments", methods=["GET"])
def get_equipments():
    return index()


@token_required
@app.route(prefix + "/equipment", methods=["GET"])
def get_equipment():
    return params()


# unused
@token_required
@app.route(prefix + "/selected-tags", methods=["GET"])
def get_selected_tags():
    return selected_tag()


# unused
@token_required
@app.route(prefix + "/tag/<int:id>", methods=["GET"])
def get_tag(id):
    return tag_by_id(id)


# unused
@token_required
@app.route(prefix + "/tags", methods=["GET"])
def get_tags():
    return tag_index()


# unused
@token_required
@app.route(prefix + "/psd-values/<int:id>", methods=["GET"])
def get_psd(id):
    return tag_psd_values(id)


@token_required
@app.route(prefix + "/equipments", methods=["POST"])
def create_equipment():
    return create()


@token_required
@app.route(prefix + "/equipment/<uuid:id>", methods=["GET", "PUT", "DELETE"])
def detail_equipment(id):
    if request.method == "GET":
        return show(str(id))
    elif request.method == "PUT":
        return update(str(id))
    elif request.method == "DELETE":
        return delete(str(id))
