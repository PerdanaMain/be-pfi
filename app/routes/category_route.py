from app import app, prefix
from app.controllers.master_category_controller import index, create, delete
from app.middlewares.token_verify import token_required


@token_required
@app.route(prefix + "/categories", methods=["GET"])
def get_categories():
    return index()


@token_required
@app.route(prefix + "/categories", methods=["POST"])
def create_category():
    return create()


@token_required
@app.route(prefix + "/category/<uuid:id>", methods=["DELETE"])
def category(id):
    return delete(id)
