from models.supplier import Supplier


def test_success_constructor():
    supplier = Supplier(name="Tom", email="abc",
                        products=[3, 4, 12, 9])
    assert supplier.name == "Tom"
    assert supplier.address == ""
    assert supplier.email == "abc"
    assert supplier.products == [3, 4, 12, 9]
    assert supplier.id is None
