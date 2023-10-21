from typing import Protocol, runtime_checkable

from functiongroup import FunctionGroup


@runtime_checkable
class MyProtocol(Protocol):

    def func_1(self, arg: int, arg_2: str) -> tuple[int, str]:
        ...

    def func_2(self, arg: int) -> int:
        ...


func_group = FunctionGroup()


@func_group.register
def func_1(arg: int, arg_2: str, common: str):
    return arg, arg_2


@func_group.register
def func_2(arg: int, common: str):
    return arg


def test_function_group():
    proto: MyProtocol = func_group(common="int")
    assert proto.func_1(1, "1") == (1, "1")
    assert proto.func_2(2) == 2
    assert isinstance(proto, MyProtocol)
