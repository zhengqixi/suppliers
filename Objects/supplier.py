'''

'''

import json
from typing import Dict
from product.py import Product


class Supplier:
    '''
    Supplier model that encapsulates
    necessary info about a supplier
    '''

    def __init__(self, name: str, id: str = None,
                 email: str = None, address: str = None,
                 products: Dict[str, Product] = {}) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the supplier
        id : str, optional
            The id of the supplier (default is None).
            Its value is obtained from the DB and needs to be set eventually
        email: str, optional
            The email of the supplier (default is None)
        address: str, optional
            The address of the supplier (default is None)
        products: Dict[str, Product], optional
            The products of the supplier (default is {})
        """

        if (email is None and address is None):
            raise MissingContactInfo("At least one contact method \
                                    (email or address) is required")

        self._id = None  # DB provides ID
        self._name = name
        self._email = email
        self._address = address
        self._products = {}

    @property
    def id(self) -> str:
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
    def products(self) -> Dict[str, Product]:
        '''products of the supplier'''
        return Dict(self._products)

    @id.setter
    def id(self, id: str) -> str:
        self._id = id

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @email.setter
    def email(self, email: int) -> None:
        self._email = email

    @address.setter
    def address(self, address: str) -> str:
        self._address = address

    @products.setter
    def products(self, products: Dict[str, Product]) -> None:
        self._products = products

    def add_product(self, product: Product) -> None:
        '''add a product to the supplier'''
        self._products[product.id()] = product

    def to_json(self) -> str:
        '''convert the supplier to JSON formatted string'''
        def formatter(supplier: Supplier):
            return {k.lstrip('_'): v for k, v in vars(supplier).items()}

        return json.dumps(self, default=formatter, indent=4)


if __name__ == "__main__":
    pass
    # s = Supplier("apple", "pear")
    # s.add_product(Apple(1))
    # s.add_product(Apple(2))
    # s.id
    # s2 = Supplier("Tom", "Ma")
    # print(s.__dict__)
    # print(s.toJSON())
    # print(s2.toJSON())
