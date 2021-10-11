"""
this file defines the model for a product
"""
import json


class Product:
    """Product class"""

    def __init__(self, name: str, price: int = None) -> None:
        self._id = None  # DB provides ID
        self._name = name
        self._price = price

    @property
    def id(self) -> str:
        """get id"""
        return self._id

    @property
    def name(self) -> str:
        """get name"""
        return self._name

    @property
    def price(self) -> int:
        """get price"""
        return self._price

    @id.setter
    def id(self, id: str) -> None:
        self._id = id

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @price.setter
    def price(self, price: int) -> None:
        self._price = price

    def to_json(self) -> str:
        """convert to JSON"""
        def formatter(product: Product):
            return {k.lstrip('_'): v for k, v in vars(product).items()}
        return json.dumps(self, default=formatter, indent=4)

# if __name__ == "__main__":
#     p = Product("tea", 10)
#     print(p.__dict__)
#     print(p.to_json())
