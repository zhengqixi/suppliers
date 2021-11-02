"""
Supplier Store Service

Paths:
------
GET /suppliers - Returns a list all of the Suppliers
GET /suppliers/{id} - Returns the Supplier with a given id number
POST /suppliers - creates a new Supplier record in the database
PUT /suppliers/{id} - updates a Supplier record in the database
DELETE /suppliers/{id} - deletes a Supplier record in the database
"""

import os
import logging
from typing import Tuple
from flask import jsonify, Response, request, make_response
from werkzeug.exceptions import abort, NotFound, BadRequest
from service import error_handlers, status, supplier, app
from service.supplier import Supplier

from . import status, app


######################################################################
# Application Routes
######################################################################
@app.route("/")
def index() -> Tuple[Response, int]:
    """ Returns a message about the service """
    app.logger.info("Request for Index page")
    message = "Hello World from Supplier team"
    return make_response(jsonify(name=message), status.HTTP_200_OK)


@app.route("/suppliers", methods=["POST"])
def create_supplier() -> Tuple[Response, int]:
    """ Creates a supplier and returns the supplier as a dict """

    check_content_type_is_json()
    request_body = request.json
    app.logger.info("request body: {}".format(request_body))

    if "name" not in request_body:
        raise BadRequest("missing name")

    new_supplier = Supplier.deserialize_from_dict(request_body)
    new_supplier.create()
    message = new_supplier.serialize_to_dict()

    app.logger.info("created new supplier with id {}".format(new_supplier.id))

    return make_response(jsonify(message), status.HTTP_201_CREATED)


@app.route("/suppliers/<int:supplier_id>", methods=["GET"])
def get_supplier(supplier_id) -> Tuple[Response, int]:
    """ Reads a supplier and returns the supplier as a dict """
    app.logger.info('Reads a supplier with id: {}'.format(supplier_id))
    supplier = Supplier.find(supplier_id)
    app.logger.info("Returning supplier: %s", supplier.name)
    message = supplier.serialize_to_dict()
    return make_response(jsonify(message), status.HTTP_200_OK)


@app.route("/suppliers/<int:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id: int) -> Tuple[Response, int]:
    """ 
    Updates a supplier with the provided supplier id 
    Returns the updated supplier 
    """
    check_content_type_is_json()
    request_body = request.json
    app.logger.info("request body: {}".format(request_body))

    supplier = Supplier.find(supplier_id)
    supplier.update(request_body)
    message = supplier.serialize_to_dict()

    return make_response(jsonify(message), status.HTTP_200_OK)


@app.route("/suppliers/<int:supplier_id>/products", methods=["POST"])
def add_product(supplier_id: int) -> Tuple[Response, int]:
    """
    Adds the provided list of products to a supplier
    Returns the updated supplier
    """
    check_content_type_is_json()
    request_body = request.json
    app.logger.info("request body: {}".format(request_body))

    supplier = Supplier.find(supplier_id)
    try:
        supplier.add_products(request_body["products"])
        message = supplier.serialize_to_dict()
        return make_response(jsonify(message), status.HTTP_200_OK)
    except KeyError:
        raise BadRequest("products not provided")


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def check_content_type_is_json():
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == "application/json":
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format("application/json"),
    )
