from app import app, prefix
from app.controllers.master_tag_controller import index, insert


@app.route(prefix + "/tags", methods=["GET"])
def get_tags():
    return index()


@app.route(prefix + "/tags", methods=["POST"])
def post_tags():
    return insert()
