import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
import logging
from typing import Tuple
from flask import jsonify, Response, request, make_response, Flask
from service import error_handlers, status, supplier, app

######################################################################
# Get bindings from the environment
######################################################################

DEBUG = os.getenv("DEBUG", "False") == "True"
PORT = os.getenv("PORT", "5000")

######################################################################
# Create Flask application
######################################################################
if DEBUG:
    app.logger.setLevel(logging.DEBUG)
else:
    app.logger.setLevel(logging.INFO)


######################################################################
# Application Routes
######################################################################
@app.route("/")
def index() -> Tuple[Response, int]:
    """ Returns a message about the service """
    app.logger.info("Request for Index page")
    return (
        jsonify(
            name="Hello World from Supplier team"
        ),
        200,
    )


@app.route("/suppliers", methods=["POST"])
def create_supplier() -> Tuple[Response, int]:
    """ Creates a supplier and returns the ID """
    request_body = request.json
    app.logger.info("request body: {}".format(request_body))

    if request_body is None:
        app.logger.info("missing body bad request")
        return error_handlers.bad_request("missing body")

    if "name" not in request_body:
        return error_handlers.bad_request("missing name")

    new_supplier = supplier.Supplier.deserialize_from_dict(request_body)
    new_supplier.create()
    message = new_supplier.serialize_to_dict()

    app.logger.info(
        "created new supplier with id {}".format(new_supplier.id))

    return make_response(jsonify(message), status.HTTP_201_CREATED)

# ######################################################################
# #   Convenience functions
# ######################################################################


# def error_response(msg: str, error_code: int) -> Tuple[Response, int]:
#     return jsonify(
#         error=msg
#     ), error_code


######################################################################
#   M A I N
######################################################################
# if __name__ == "__main__":
#     app.logger.info("*" * 70)
#     app.logger.info("   Seleton Flask For Supplier   ".center(70, "*"))
#     app.logger.info("*" * 70)
#     app.run(host="0.0.0.0", port=int(PORT), debug=DEBUG)

    #test_routes.TestSupplierServer.test_create_supplier()
