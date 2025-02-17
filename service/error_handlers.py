from flask import jsonify
from . import app, status
from service.supplier_exception import SupplierException


@app.errorhandler(SupplierException)
def supplier_exception(error):
    """ Handles supplier exceptions as bad requests """
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad requests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_400_BAD_REQUEST, error=message),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handles not found responses """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error=message),
        status.HTTP_404_NOT_FOUND,
    )
