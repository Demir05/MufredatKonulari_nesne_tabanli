from typing import Tuple,Dict,Callable,Any,NamedTuple
import string,operator
from collections import namedtuple as np



IMMUTABLE:Tuple[type,...] = (str,tuple,frozenset,type(None),bool,int,float)
ASCII_LETTERS = string.ascii_letters
ASCII_DIGITS = string.digits
ASCII_CHARS = string.ascii_letters + ASCII_DIGITS
ASCII_LOWERCASE = string.ascii_lowercase
ASCII_UPPERCASE = string.ascii_uppercase

def generate_func(a,b,operator,/):
    return f"{a} {operator} {b}"


operator_functions:Dict[str,Callable[...,Any]] = {
    "__add__":operator.add,
    "__sub__":operator.sub,
    "__mul__":operator.mul,
    "__truediv__":operator.truediv,
    "__floordiv__":operator.floordiv,
    "__mod__":operator.mod,
    "__pow__":operator.pow,
}

operator_inline_functions:Dict[str,Callable[...,Any]] = {
    "__iadd__":operator.iadd,
    "__isub__":operator.isub,
    "__imul__":operator.imul,
    "__itruediv__":operator.itruediv,
    "__ifloordiv__":operator.ifloordiv,
    "__imod__":operator.imod,
    "__ipow__":operator.ipow,
}
operator_fallback:Dict[str,Callable[...,Any]] = dict.fromkeys(("__radd__","__rsub__","__rmul__","__rpow__","__rtruediv__","__rfloordiv__"),generate_func)

exceptions:Dict[str,Callable[[Exception],None]] = {
    "inject_error":lambda err:print(f"Error: injection Error >>> {err}"),
    "operator_not_found":lambda err:print(f"Error: operator could not found Error >>> {err}"),
}

Exp = np("Exp",["inject_error","operator_not_found"])

exp:Exp = Exp(
    inject_error=exceptions["inject_error"],
    operator_not_found = exceptions["operator_not_found"],
)

class ManagerExpections:
    def __init__(self):
        self.exp = exp



