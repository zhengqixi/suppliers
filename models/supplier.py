'''
This file defines the model for Supplier
'''

import json
from typing import List, Set, Union
from exceptions.supplier_exception \
    import MissingContactInfo, MissingProductId, WrongArgType, OutOfRange


class Supplier:
    '''
    Supplier model that encapsulates
    necessary info about a supplier
    '''

    def __init__(self, name: str, id: int = None,
                 email: str = "", address: str = "",
                 products: Union[List[int], Set[int]] = []) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the supplier
        id : int (0, 1e10), optional
            The id of the supplier (default is None).
            Its value is obtained from the DB and needs to be set eventually
        email: str, optional
            The email of the supplier (default is None)
        address: str, optional
            The address of the supplier (default is None)
        products: Union[List[Product], Set[Product]], optional
            The products of the supplier (default is [])
        """
        if id is not None:
            self._check_id(id)
        self._check_name(name)
        self._check_email(email)
        self._check_address(address)
        self._check_products(products)
        if (email == "" and address == ""):
            raise MissingContactInfo("At least one contact method "
                                     "(email or address) is required")

        self._id = id
        self._name = name
        self._email = email
        self._address = address
        self._products = list(products)

    @property
    def id(self) -> int:
        '''id of the supplier'''
        return self._id

    @property
    def name(self) -> str:
        '''name of the supplier'''
        return self._name

    @property
    def email(self) -> int:
        '''email of the supplier'''
        return self._email

    @property
    def address(self) -> str:
        '''address of the supplier'''
        return self._address

    @property
    def products(self) -> List[int]:
        '''products of the supplier'''
        return self._products

    @id.setter
    def id(self, id: int) -> None:
        self._check_id(id)
        self._id = id

    @name.setter
    def name(self, name: str) -> None:
        self._check_name(name)
        self._name = name

    @email.setter
    def email(self, email: str) -> None:
        self._check_email(email)
        self._email = email

    @address.setter
    def address(self, address: str) -> None:
        self._check_address(address)
        self._address = address

    @products.setter
    def products(self, products: Union[List[int], Set[int]]) -> None:
        self._check_products(products)
        self._products = products

    def add_product(self, product: int) -> None:
        '''add a product to the supplier'''
        self._check_product(product)
        if product is None:
            raise MissingProductId("Product has no id")
        self._products.append(product)

    def to_json(self) -> str:
        '''convert the supplier to JSON formatted string'''
        def formatter(supplier: Supplier):
            return {k.lstrip('_'): v for k, v in vars(supplier).items()}
        return json.dumps(self, default=formatter, indent=4)

    def _check_id(self, id: int) -> None:
        '''check the type and the range of id'''
        if not isinstance(id, int):
            raise WrongArgType("<class 'int'> expected for id, "
                               "got %s" % type(id))
        elif (id >= 1e10 or id <= 0):
            raise OutOfRange("supplier id is not within range (0, 1e10), "
                             "got %s" % id)

    def _check_name(self, name: str) -> None:
        '''check the type of name'''
        if not isinstance(name, str):
            raise WrongArgType("<class 'str'> expected for name, "
                               "got %s" % type(name))

    def _check_email(self, email: str) -> None:
        '''check the type of email'''
        # email format parser may needed
        if not isinstance(email, str):
            raise WrongArgType("<class 'str'> expected for email, "
                               "got %s" % type(email))
        if (email == "" and self._address == ""):
            raise MissingContactInfo("At least one contact method "
                                     "(email or address) is required")

    def _check_address(self, address: str) -> None:
        '''check the type of address'''
        if not isinstance(address, str):
            raise WrongArgType("<class 'str'> expected for address, "
                               "got %s" % type(address))
        if (self._email == "" and address == ""):
            raise MissingContactInfo("At least one contact method "
                                     "(email or address) is required")

    def _check_product(self, product: int) -> None:
        '''check the type and the range of product id'''
        if not isinstance(product, int):
            raise WrongArgType("class<'int'> expected for product id, "
                               "got %s" % type(product))
        elif (product >= 1e15 or product <= 0):
            raise OutOfRange("product id is not within range (0, 1e15), "
                             "got %s" % id)

    def _check_products(self, products:
                        Union[List[int], Set[int]]) -> None:
        '''check the type of products'''
        if not isinstance(products, (List, Set)):
            raise WrongArgType("class<'List'> or class<'Set'> expected "
                               "for products, got %s" % type(products))
        for p in products:
            self._check_product(p)
