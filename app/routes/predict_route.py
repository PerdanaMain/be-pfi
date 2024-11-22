import json
import time

from flask import Response, request
from app import app, prefix
from app.middlewares.token_verify import token_required
from app.controllers.prediction_controller import (
    index,
    stream_tag_value,
    stream_tag_prediction_value,
)


@token_required
@app.route(prefix + "/predict-values", methods=["GET"])
def predict_values():
    return index()


@token_required
@app.route(prefix + "/stream-values", methods=["GET"])
def stream_values():
    """
    Endpoint untuk streaming data ke client menggunakan Server-Sent Events.
    """
    try:
        # Ambil parameter `tag_id`
        tag_id = request.args.get("tag_id", default=1, type=int)
        return Response(stream_tag_value(tag_id), content_type="text/event-stream")
    except Exception as e:
        # Format error response
        error_data = {"error": str(e)}
        return Response(
            f"data: {json.dumps(error_data)}\n\n", content_type="text/event-stream"
        )


@token_required
@app.route(prefix + "/stream-prediction-values", methods=["GET"])
def stream_prediction_values():
    """
    Endpoint untuk streaming data ke client menggunakan Server-Sent Events.
    """
    try:
        # Ambil parameter `tag_id`
        tag_id = request.args.get("tag_id", default=1, type=int)
        return Response(
            stream_tag_prediction_value(tag_id), content_type="text/event-stream"
        )
    except Exception as e:
        # Format error response
        error_data = {"error": str(e)}
        return Response(
            f"data: {json.dumps(error_data)}\n\n", content_type="text/event-stream"
        )
