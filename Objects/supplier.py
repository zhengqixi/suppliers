import json
from typing import Dict
#from product.py import Product

class Apple:
    def __init__(self, id) -> None:
        self.name = "apple"
        self.index = str(id)

    def getId(self):
        return self.index

class Supplier:
    def __init__(self, fname: str, lname: str, age: int = None, address: str = None) -> None:
        self._id = None # DB provides ID
        self._fname = fname
        self._lname = lname
        self._age = age
        self._address = address
        self._products = {}

    def addProduct(self, product: Apple) -> None:
        self._products[product.getId()] = product

    @property
    def id(self) -> str:
        return self._id

    @property
    def fname(self) -> str:
        return self._fname
    
    @property 
    def lname(self) -> str:
        return self._lname
    
    @property
    def age(self) -> int:
        return self._age
    
    @property
    def address(self) -> str:
        return self._address

    @property
    def products(self) -> Dict[str, Apple]:
        return Dict(self._products)
    
    @fname.setter
    def fname(self, fname: str) -> None:
        self._fname = fname

    @lname.setter
    def lname(self, lname: str) -> None:
        self._lname = lname

    @age.setter
    def age(self, age: int) -> None:
        self._age = age

    @address.setter
    def address(self, address: str) -> str:
        self._address = address

    @products.setter
    def products(self, products: Dict[str, Apple]) -> None:
        self._products = products

    def toJSON(self) -> str:
        return json.dumps(self, default = lambda o: {k.lstrip('_'): v for k, v in vars(o).items()}, indent = 4)

if __name__ == "__main__":
    s = Supplier("apple", "pear")
    s.addProduct(Apple(1))
    s.addProduct(Apple(2))
    s.id
    s2 = Supplier("Tom", "Ma")
    print(s.__dict__)
    print(s.toJSON())
    print(s2.toJSON())
