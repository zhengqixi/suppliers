class MissingContactInfo(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class WrongArgType(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class OutOfRange(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MissingProductId(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
