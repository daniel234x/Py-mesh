import pytest

from .. import *

def test_int():
    values = [0, 1, 8, 232323, 2**64 - 1]

    for value in values:
        expr = Int(value)
        assert expr.type_of() == TealType.uint64

        expected = TealSimpleBlock([
            TealOp(Op.int, value)
        ])

        actual, _ = expr.__teal__()

        assert actual == expected

def test_int_invalid():
    with pytest.raises(TealInputError):
        Int(6.7)

    with pytest.raises(TealInputError):
        Int(-1)

    with pytest.raises(TealInputError):
        Int(2 ** 64)
    
    with pytest.raises(TealInputError):
        Int("0")

def test_enum_int():
    expr = EnumInt("OptIn")
    assert expr.type_of() == TealType.uint64
    
    expected = TealSimpleBlock([
        TealOp(Op.int, "OptIn")
    ])

    actual, _ = expr.__teal__()

    assert actual == expected
