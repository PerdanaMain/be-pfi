from app import app, prefix
from app.middlewares.token_verify import token_required
from app.controllers.master_equipment_controller import (
    report_equipments,
)


@app.route(prefix + "/schedule/envelope-fetch", methods=["GET"])
@token_required
def get_schedule_envelope_fetch():
    return report_equipments()


@app.route(prefix + "/schedule/value-tag", methods=["GET"])
@token_required
def get_schedule_value_tag():
    return report_equipments()
