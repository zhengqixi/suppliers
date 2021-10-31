"""
Test cases for Supplier Model
Test cases can be run with:
    nosetests
    coverage report -m
While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_suppliers.py:TestSupplierModel
"""
import os
import unittest
from werkzeug.exceptions import NotFound
from service.supplier import Supplier, db
from service import app
import logging
from service.supplier_exception \
    import MissingInfo, OutOfRange, WrongArgType, UserDefinedIdError

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  S U P P L I E R   M O D E L   T E S T   C A S E S
######################################################################
class TestSupplierModel(unittest.TestCase):
    """Test Cases for Supplier Model"""
    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Supplier.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def supplier_repr(self):
        supplier = Supplier(name='foo', address="USA")
        supplier.create()
        print(supplier)
        self.assertEqual(repr(supplier), "<Supplier foo, id=1>")

    def test_construct_a_supplier(self):
        """Create a supplier and assert that it exists"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com")
        self.assertTrue(supplier is not None)
        self.assertEqual(supplier.id, None)
        self.assertEqual(supplier.name, "Tom")
        self.assertEqual(supplier.email, "Tom@gmail.com")
        self.assertEqual(supplier.address, None)
        self.assertEqual(supplier.products, None)
        supplier = Supplier(name="Apple",
                            email="abc@apple.com",
                            products=[1, 2, 3])
        self.assertEqual(supplier.name, "Apple")
        self.assertEqual(supplier.email, "abc@apple.com")
        self.assertEqual(supplier.products, [1, 2, 3])

    def test_construct_supplier_with_insufficient_info(self):
        '''construct a supplier with insufficient info'''
        self.assertRaises(MissingInfo, Supplier, name="Tom", products=[1, 2])
        self.assertRaises(MissingInfo, Supplier, name=None, address="US")

    def test_construct_supplier_with_wrong_type_input(self):
        '''construct a supplier with input of wrong type'''
        self.assertRaises(WrongArgType, Supplier, name=1, address="US")
        self.assertRaises(WrongArgType, Supplier, name="Tom", address=1)
        self.assertRaises(WrongArgType, Supplier, name="foo", email=1)
        self.assertRaises(WrongArgType, Supplier, name="foo",
                          email="abc", products=["d"])
        self.assertRaises(WrongArgType, Supplier, name="foo",
                          email="abc", products=1)

    def test_construct_supplier_with_invalid_product_id(self):
        self.assertRaises(OutOfRange, Supplier, name="foo",
                          email="abc", products=[-2])

    def test_construct_supplier_with_user_defined_id(self):
        '''construct a supplier with user defined id'''
        self.assertRaises(UserDefinedIdError, Supplier,
                          id=2, name="Tom", address="US")

    def test_serialization_to_dict(self):
        """Convert a supplier object to a dict object"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[1, 5])
        output = supplier.serialize_to_dict()
        self.assertTrue(isinstance(output, dict))
        self.assertEqual(output["name"], "Tom")
        self.assertEqual(output["email"], "Tom@gmail.com")
        self.assertEqual(output["products"], [1, 5])

    def test_deserialization_from_dict(self):
        """Convert a dict object to a supplier object"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[1, 5])
        dictionary = supplier.serialize_to_dict()
        other = Supplier.deserialize_from_dict(dictionary)
        self.assertEqual(supplier, other)

    def test_deserialize_from_dict_missing_data(self):
        """Test deserialization from dict of a supplier with missing data"""
        data = {"address": "USA"}
        self.assertRaises(MissingInfo,
                          Supplier.deserialize_from_dict, data=data)

    def test_deserialize_from_dict_bad_data(self):
        """Test deserialization from dict of bad data"""
        data = "this is not a dictionary"
        self.assertRaises(WrongArgType,
                          Supplier.deserialize_from_dict, data=data)

    def test_deserialize_from_json_missing_data(self):
        """Test deserialization from json of a supplier with missing data"""
        json_data = "{\"name\":\"Tom\"}"
        self.assertRaises(MissingInfo,
                          Supplier.deserialize_from_json, data=json_data)

    def test_deserialize_from_json_bad_data(self):
        """Test deserialization from json of a supplier with bad data"""
        json_data = [1, 2, 3]
        self.assertRaises(WrongArgType,
                          Supplier.deserialize_from_json, data=json_data)

    def test_json_converter(self):
        """Convert a supplier object to JSON string and vice versas"""
        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[1, 5])
        json_output = supplier.serialize_to_json()
        other = Supplier.deserialize_from_json(json_output)
        self.assertEqual(supplier, other)
        pass

    def test_create_suppliers(self):
        """Create a supplier and add it to the database"""
        suppliers = Supplier.all()
        self.assertEqual(suppliers, [])

        supplier = Supplier(name="Ken",
                            email="Ken@gmail.com", products=set([2, 4]))
        self.assertEqual(supplier.id, None)
        supplier.create()
        self.assertEqual(supplier.id, 1)
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 1)

        supplier = Supplier(name="Tom", email="Tom@gmail.com", products=[11])
        self.assertEqual(supplier.id, None)
        supplier.create()
        self.assertEqual(supplier.id, 2)
        suppliers = Supplier.all()
        self.assertEqual(len(suppliers), 2)

    def test_find_supplier(self):
        """Find a Supplier by ID"""
        suppliers = [
        Supplier(name="abc", email="abc@gmail.com", products=[1, 2, 3]),
        Supplier(name="def", email="def@gmail.com", address="nyu", products=[4, 5]),
        Supplier(name="gh", address="new york", products=[6, 7])
        ]
        for supplier in suppliers:
            supplier.create()
        logging.debug(suppliers)
        # make sure they got saved
        self.assertEqual(len(Supplier.all()), 3)
        # find the 2nd supplier in the list
        supplier = Supplier.find(suppliers[1].id)
        self.assertIsNot(supplier, None)
        self.assertEqual(supplier.id, suppliers[1].id)
        self.assertEqual(supplier.name, suppliers[1].name)
        self.assertEqual(supplier.email, supplier[1].email)
        self.assertEqual(supplier.products, supplier[1].products)

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        suppliers = [
        Supplier(name="abc", email="abc@gmail.com", products=[1, 2, 3]),
        Supplier(name="def", email="def@gmail.com", address="nyu", products=[4, 5]),
        Supplier(name="gh", address="new york", products=[6, 7])
        ]
        for supplier in suppliers:
            supplier.create()
        logging.debug(suppliers)
        # make sure they got saved
        self.assertEqual(len(Supplier.all()), 3)
        # find the 2nd supplier in the list
        supplier = Supplier.find_or_404(suppliers[1].id)
        self.assertIsNot(supplier, None)
        self.assertEqual(supplier.id, suppliers[1].id)
        self.assertEqual(supplier.name, suppliers[1].name)
        self.assertEqual(supplier.email, supplier[1].email)
        self.assertEqual(supplier.products, supplier[1].products)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Supplier.find_or_404, 0)

