from app import app, prefix
from app.controllers.value_tag_controller import search, mass_insert


@app.route(prefix + "/tag-values", methods=["GET"])
def get_value():
    return search()


@app.route(prefix + "/tag-values", methods=["POST"])
def create_value():
    return mass_insert()
