from app import app, prefix
from app.middlewares.token_verify import token_required
from app.controllers.master_category_controller import index, create, delete


@app.before_request
@token_required
def before_request():
    pass


@app.route(prefix + "/categories", methods=["GET"])
def get_categories():
    return index()


@app.route(prefix + "/categories", methods=["POST"])
def create_category():
    return create()


@app.route(prefix + "/category/<uuid:id>", methods=["DELETE"])
def category(id):
    return delete(id)
