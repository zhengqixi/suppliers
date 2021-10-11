import os
import logging
from typing import Tuple
from flask import Flask, jsonify, Response


######################################################################
# Get bindings from the environment
######################################################################
DEBUG = os.getenv("DEBUG", "False") == "True"
PORT = os.getenv("PORT", "5000")


######################################################################
# Create Flask application
######################################################################
app = Flask(__name__)
app.logger.setLevel(logging.INFO)


######################################################################
# Storage for Suppliers
######################################################################
suppliers = []


######################################################################
# Application Routes
######################################################################
@app.route("/")
def index() -> Tuple[Response, int]:
    """ Returns a message about the service """
    app.logger.info("Request for Index page")
    return (
        jsonify(
            name="Supplier"
        ),
        200,
    )


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    app.logger.info("*" * 70)
    app.logger.info("   Seleton Flask For Supplier   ".center(70, "*"))
    app.logger.info("*" * 70)
    app.run(host="0.0.0.0", port=int(PORT), debug=DEBUG)
