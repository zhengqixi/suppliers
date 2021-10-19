from models.supplier import Supplier
from exceptions.supplier_exception\
    import OutOfRange, MissingContactInfo, WrongArgType


def test_create_supplier_valid_params():
    supplier = Supplier(
        name='test',
        email='test',
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
        Supplier(
            name='test',
            products=[1, 2, 3]
        )
    except Exception as e:
        assert isinstance(e, MissingContactInfo)


def test_create_supplier_invalid_products():
    try:
        Supplier(
            name='test',
            email='test',
            products=['complete garbage']
        )
    except Exception as e:
        assert isinstance(e, WrongArgType)


def test_create_supplier_invalid_products_container():
    try:
        Supplier(
            name='test',
            email='test',
            products='absolute garbage'
        )
    except Exception as e:
        assert isinstance(e, WrongArgType)


def test_create_supplier_invalid_name():
    try:
        Supplier(
            name=177013,
            email='test',
        )
    except Exception as e:
        assert isinstance(e, WrongArgType)


def test_create_supplier_invalid_email():
    try:
        Supplier(
            name='test',
            email=177013,
        )
    except Exception as e:
        assert isinstance(e, WrongArgType)


def test_create_supplier_invalid_id():
    try:
        Supplier(
            name='test',
            email='test',
            id=100000000000000
        )
    except Exception as e:
        assert isinstance(e, OutOfRange)


def test_update_supplier_invalid_id():
    supplier = Supplier(
            name='test',
            email='test',
        )
    try:
        supplier.id = -3
    except Exception as e:
        assert isinstance(e, OutOfRange)


def test_update_supplier_invalid_name():
    supplier = Supplier(
            name='test',
            email='test',
        )
    try:
        supplier.name = []
    except Exception as e:
        assert isinstance(e, WrongArgType)


def test_update_supplier_invalid_email():
    supplier = Supplier(
            name='test',
            email='test',
        )
    try:
        supplier.email = ""
    except Exception as e:
        assert isinstance(e, MissingContactInfo)
    try:
        supplier.email = 2
    except Exception as e:
        assert isinstance(e, WrongArgType)


def test_update_supplier_invalid_address():
    supplier = Supplier(
            name='test',
            address='test',
        )
    try:
        supplier.address = ""
    except Exception as e:
        assert isinstance(e, MissingContactInfo)
    try:
        supplier.address = 2
    except Exception as e:
        assert isinstance(e, WrongArgType)


def test_update_supplier_invalid_products():
    supplier = Supplier(
            name='test',
            email='test',
        )
    try:
        supplier.products = "test"
    except Exception as e:
        assert isinstance(e, WrongArgType)


def test_add_valid_product():
    supplier = Supplier(
            name='test',
            email='test',
        )
    supplier.add_product(2)

    assert supplier.products == [2]


def test_add_invalid_product():
    supplier = Supplier(
            name='test',
            email='test',
        )
    try:
        supplier.add_product("2")
    except Exception as e:
        assert isinstance(e, WrongArgType)


def test_to_json():
    supplier = Supplier(
        name='test',
        email='test',
        products=[1, 2, 3]
    )
    assert supplier is not None
    json_str = supplier.to_json()
    assert json_str != ""
