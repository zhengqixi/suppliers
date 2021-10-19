from exceptions.supplier_exception\
    import MissingContactInfo, WrongArgType, OutOfRange


def test_raise_missing_contact_info():
    try:
        raise MissingContactInfo()
    except MissingContactInfo:
        assert True is True


def test_raise_wrong_arg_type():
    try:
        raise WrongArgType()
    except WrongArgType:
        assert True is True


def test_raise_out_of_range():
    try:
        raise OutOfRange()
    except OutOfRange:
        assert True is True
