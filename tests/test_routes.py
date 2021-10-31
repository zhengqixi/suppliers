import os
import logging
import unittest


from service import status  # HTTP Status Codes
from service.supplier import db, init_db
from service.routes import app

# Disable all but ciritcal errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/suppliers"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################


class TestSupplierServer(unittest.TestCase):
    """Supplier Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Hello World from Supplier team")

    def test_create_supplier(self):
        """Create a new Supplier for testing"""
        test_supplier = {
            "name": "TOM",
            "email": "a0",
            "address": "asd",
            "products": [102, 123],
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Check the data is correct
        resp_supplier = resp.get_json()
        self.assertEqual(
            resp_supplier["name"], test_supplier["name"], "Names do not match")
        self.assertEqual(
            resp_supplier["email"], test_supplier["email"], "Email do not match"
        )
        self.assertEqual(
            resp_supplier["address"], test_supplier["address"], "Address does not match"
        )
        self.assertEqual(
            resp_supplier["products"], test_supplier["products"], "Products does not match"
        )

    def test_create_supplier_without_name(self):
        """Create a Supplier with no name"""
        test_supplier = {
            "email": "a0@purdue.edu",
            "address": "asd",
            "products": [102, 123],
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_supplier_without_content_type(self):
        """Create a Supplier with no content type"""
        resp = self.app.post(BASE_URL)
        self.assertEqual(resp.status_code,
                         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_supplier_invalid_arguments(self):
        """ Create a Supplier with a user supplied id """
        test_supplier = {
            "email": "test@nyu.edu",
            "address": "omg",
            "id": 2
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_supplier_happy_path(self):
        """ Create a supplier and update it """

        # Create supplier
        test_supplier = {
            "name": "TOM",
            "email": "a0",
            "address": "asd",
            "products": [102, 123],
        }
        logging.debug(test_supplier)
        resp = self.app.post(
            BASE_URL, json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Update the fields
        test_supplier = {
            "email": "test@nyu.edu",
            "address": "omg",
        }
        logging.debug(test_supplier)
        resp = self.app.put(
            "{}/{}".format(BASE_URL, resp.json["id"]), json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        body = resp.json
        self.assertEqual(body["email"], "test@nyu.edu")
        self.assertEqual(body["address"], "omg")
        # Verify that the other fields have not changed
        self.assertEqual(body["name"], "TOM")
        self.assertEqual(body["products"], [102, 123])

    def test_update_supplier_does_not_exist(self):
        """ Update a supplier which does not exist """
        test_supplier = {
            "email": "test@nyu.edu",
            "address": "omg",
        }
        logging.debug(test_supplier)
        resp = self.app.put(
            "{}/{}".format(BASE_URL, 0), json=test_supplier, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
