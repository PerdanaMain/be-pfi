from app import app, prefix
from app.middlewares.token_verify import token_required
from app.services.response import *
from app.controllers.chart_controller import *


@token_required
@app.route(prefix + "/chart/information", methods=["GET"])
def get_information():
    return information_chart()
