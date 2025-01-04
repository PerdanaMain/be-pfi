from flask import request
import requests
from app.config.config import Config
from functools import wraps
from app.services.response import unauthorized, forbidden, bad_request


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        auth = Config.AUTH_SERVICE_ENDPOINT
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            return unauthorized(False, "Token is missing", None)

        try:
            payload = requests.get(
                auth + "/verify-token",
                headers={"Authorization": token},
            )
            if payload.status_code != 200:
                return forbidden(False, "Token is invalid", None)

        except Exception as e:
            return bad_request(False, f"Error while checking token: {e}", None)

        return f(*args, **kwargs)

    return decorator
