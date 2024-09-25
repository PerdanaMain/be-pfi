from app import app, prefix
from app.controllers.master_equipment_controller import index


@app.route(prefix + "/equipments", methods=["GET"])
def get_equipments():
    return index()
