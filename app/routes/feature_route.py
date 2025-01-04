from app import app, prefix
from flask import request
from app.middlewares.token_verify import token_required
from app.controllers.feature_controller import index, show, store, update, destroy


@token_required
@app.route(prefix + "/features", methods=["GET"])
def get_feature():
    return index()


@token_required
@app.route(prefix + "/features", methods=["POST"])
def post_feature():
    return store(request.json)


@token_required
@app.route(prefix + "/features/<uuid:id>", methods=["GET", "PUT", "DELETE"])
def detail_feature(id):
    if request.method == "GET":
        return show(str(id))
    elif request.method == "PUT":
        return update(str(id), request.json)
    elif request.method == "DELETE":
        return destroy(str(id))
