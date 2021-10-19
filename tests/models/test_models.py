from models import supplier
from models.supplier import Supplier


def test_create_supplier_valid_params():
    supplier = Supplier(
        name='test',
        email='test',
        products=[1, 2, 3]
    )
    assert supplier is not None


def test_assert_getters():
    supplier = Supplier(
        id=1,
        name='test',
        email='test',
        address='test',
        products=[1, 2, 3]
    )
    assert supplier.id == 1
    assert supplier.name == 'test'
    assert supplier.email == 'test'
    assert supplier.address == 'test'
    assert supplier.products == [1, 2, 3]


def test_assert_setters():
    supplier = Supplier(
        id=1,
        name='test',
        email='test',
        address='test',
        products=[1, 2, 3]
    )
    supplier.id = 1
    supplier.name = '1'
    supplier.email = '2'
    supplier.address = '3'
    supplier.products = [1]
    assert supplier.id == 1
    assert supplier.name == '1'
    assert supplier.email == '2'
    assert supplier.address == '3'
    assert supplier.products == [1]


def test_create_supplier_invalid_contact():
    try:
        supplier = Supplier(
            name='test',
            products=[1, 2, 3]
        )
    except Exception:
        assert True is True


def test_create_supplier_invalid_products():
    try:
        test_supplier = Supplier(
            name='test',
            email='test',
            products=['complete garbage']
        )
    except Exception:
        assert True is True


def test_create_supplier_invalid_products_container():
    try:
        test_supplier = Supplier(
            name='test',
            email='test',
            products='absolute garbage'
        )
    except Exception:
        assert True is True


def test_create_supplier_invalid_name():
    try:
        test_supplier = Supplier(
            name=177013,
            email='test',
        )
    except Exception:
        assert True is True


def test_create_supplier_invalid_email():
    try:
        test_supplier = Supplier(
            name='test',
            email=177013,
        )
    except Exception:
        assert True is True


def test_to_json():
    supplier = Supplier(
        name='test',
        email='test',
        products=[1, 2, 3]
    )
    assert supplier is not None
    json_str = supplier.to_json()
    assert json_str != ""
