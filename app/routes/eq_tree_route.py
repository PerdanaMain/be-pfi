from app import app, prefix
from flask import request
from app.controllers.eq_tree_controller import (
    index,
    create,
    show,
    update,
    delete,
)


@app.route(prefix + "/equipment_trees", methods=["GET"])
def get_trees():
    return index()


@app.route(prefix + "/equipment_trees", methods=["POST"])
def create_trees():
    return create()


@app.route(prefix + "/equipment_tree/<uuid:id>", methods=["GET", "PUT", "DELETE"])
def detail_trees(id):
    if request.method == "GET":
        return show(id)
    elif request.method == "PUT":
        return update(id)
    elif request.method == "DELETE":
        return delete(id)
