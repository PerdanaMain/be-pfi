from app import app, prefix
from app.middlewares.token_verify import token_required
from app.controllers.master_equipment_controller import (
    report_equipments,
    filtered_report_equipments,
)


@token_required
@app.route(prefix + "/report/equipments", methods=["GET"])
def get_report_equipments():
    return report_equipments()


@token_required
@app.route(prefix + "/report/equipments/filtered", methods=["GET"])
def get_filtered_report_equipments():
    return filtered_report_equipments()
