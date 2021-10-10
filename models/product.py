import json

class Product:
    def __init__(self, name: str, price: int = None) -> None:
        self._id = None  # DB provides ID
        self._name = name
        self._price = price

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> int:
        return self._price

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @price.setter
    def price(self, price: int) -> None:
        self._price = price

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: {k.lstrip('_'): v for k, v in vars(o).items()}, indent=4)

# if __name__ == "__main__":
#     p = Product("tea", 10)
#     print(p.__dict__)
#     print(p.toJSON())
