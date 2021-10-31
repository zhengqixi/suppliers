from flask import jsonify
from . import app, status


######################################################################
# Error Handlers
######################################################################
@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handles bad reuests with 400_BAD_REQUEST"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_400_BAD_REQUEST, error=message),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handles resources not found with 404_NOT_FOUND"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error=message),
        status.HTTP_404_NOT_FOUND,
    )
