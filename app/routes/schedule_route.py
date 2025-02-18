from app import app, prefix
from app.middlewares.token_verify import token_required
from app.controllers.envelope_controller import index, feature


@app.route(prefix + "/schedule/envelope-fetch", methods=["GET"])
def get_schedule_envelope_fetch():
    return index()


@app.route(prefix + "/schedule/envelope-feature", methods=["GET"])
def get_schedule_envelope_feature():
    return feature()


@app.route(prefix + "/schedule/value-tag", methods=["GET"])
def get_schedule_value_tag():
    return index()
