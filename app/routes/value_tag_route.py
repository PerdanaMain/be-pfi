from app import app, prefix
from app.controllers.value_tag_controller import search


@app.route(prefix + "/tag-values", methods=["GET"])
def get_value():
    return search()
