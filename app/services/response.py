from flask import jsonify, make_response


def success(status, message, data):
    return make_response(
        jsonify(
            {
                "status": status,
                "message": message,
                "data": data,
            }
        ),
        200,
    )


def created(status, message, data):
    return make_response(
        jsonify(
            {
                "status": status,
                "message": message,
                "data": data,
            }
        ),
        201,
    )


def not_found(status, message, data):
    return make_response(
        jsonify(
            {
                "status": status,
                "message": message,
                "data": data,
            }
        ),
        404,
    )


def bad_request(status, message, data):
    return make_response(
        jsonify(
            {
                "status": status,
                "message": message,
                "data": data,
            }
        ),
        500,
    )


def forbidden(status, message, data):
    return make_response(
        jsonify(
            {
                "status": status,
                "message": message,
                "data": data,
            }
        ),
        403,
    )


def unauthorized(status, message, data):
    return make_response(
        jsonify(
            {
                "status": status,
                "message": message,
                "data": data,
            }
        ),
        401,
    )
