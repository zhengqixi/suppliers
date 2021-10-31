from flask import jsonify
from . import app, status


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handles bad reuests with 400_BAD_REQUEST"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_400_BAD_REQUEST, error=message),
        status.HTTP_400_BAD_REQUEST,
    )