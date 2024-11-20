from app import app, prefix
from app.middlewares.token_verify import token_required
from app.controllers.prediction_controller import index


@token_required
@app.route(prefix + "/predict-values", methods=["GET"])
def predict_values():
    return index()
