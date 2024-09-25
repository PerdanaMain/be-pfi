from app import app, prefix
from app.controllers.master_equipment_controller import index, create


@app.route(prefix + "/equipments", methods=["GET"])
def get_equipments():
    return index()


@app.route(prefix + "/equipments", methods=["POST"])
def create_equipment():
    return create()
