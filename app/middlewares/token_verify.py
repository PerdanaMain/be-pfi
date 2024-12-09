from flask import request
import requests
from app.config.config import Config
from functools import wraps
from app.services.response import unauthorized, forbidden, bad_request


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            return unauthorized(False, "Token is missing", None)

        try:
            payload = requests.get(
                Config.AUTH_SERVICE_ENDPOINT + "/verify-token",
                headers={"Authorization": "Bearer " + token},
            )
            print(payload.status_code)
            if not payload.status_code != 200:
                return forbidden(False, "Invalid token", None)

        except Exception as e:
            return bad_request(False, f"Error while checking token: {e}", None)

        return f(*args, **kwargs)

    return decorator
