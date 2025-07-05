from typing import Tuple, Dict, Callable, Any, NamedTuple, TypeVar, Union, Optional
import string,operator
from collections import namedtuple as np

T = TypeVar('T')

IMMUTABLE:Tuple[type,...] = (str,tuple,frozenset,type(None),bool,int,float)
ASCII_LETTERS:str = string.ascii_letters
ASCII_DIGITS:str = string.digits
ASCII_CHARS:str = string.ascii_letters + ASCII_DIGITS
ASCII_LOWERCASE:str = string.ascii_lowercase
ASCII_UPPERCASE:str = string.ascii_uppercase

def generate_func(self:T,other:Any,/) -> str:
    return f"Right-hand operation triggered:{type(other).__name__} used with {type(self).__name__}"


operator_functions:Dict[str,Callable[[Any,Any],Any]] = {
    "__add__":operator.add,
    "__sub__":operator.sub,
    "__mul__":operator.mul,
    "__truediv__":operator.truediv,
    "__floordiv__":operator.floordiv,
    "__mod__":operator.mod,
    "__pow__":operator.pow,
}

operator_inline_functions:Dict[str,Callable[[Any,Any],Any]] = {
    "__iadd__":operator.iadd,
    "__isub__":operator.isub,
    "__imul__":operator.imul,
    "__itruediv__":operator.itruediv,
    "__ifloordiv__":operator.ifloordiv,
    "__imod__":operator.imod,
    "__ipow__":operator.ipow,
}

operator_fallback:Dict[str,Callable[[T,Any],Any]] = dict.fromkeys(("__radd__","__rsub__","__rmul__","__rpow__","__rtruediv__","__rfloordiv__"),generate_func)

exceptions:Dict[str,Callable[[Union[Exception,Tuple[T,str]]],Optional[str]]] = {
    "inject_error":lambda err:print(f"Error: injection Error >>> {err}"),
    "operator_not_found":lambda err:print(f"Error: operator could not found Error >>> {err}"),
    "operator_attribute_error": lambda self,target:f"Error operator attribute error >>> class: {type(self)} instance: {self} not found {target} "

}

info_table:Dict[str,Callable[[T,Any],str]]= {
    "right_hand_operator": lambda self,other:f"Right-hand operation triggered:{type(other).__name__} used with {type(self).__name__}"
}

Exp = np("Exp",["inject_error","operator_not_found","operator_attribute_error"])
Info = np("Info",["right_hand_operator"])
exp:Exp = Exp(
    inject_error=exceptions["inject_error"],
    operator_not_found = exceptions["operator_not_found"],
    operator_attribute_error=exceptions["operator_attribute_error"],
)
info:Info = Info(
    right_hand_operator=info_table["right_hand_operator"]
)

class ManagerExpections:
    def __init__(self) -> None:
        self.exp:NamedTuple = exp
        self.Info:NamedTuple = info

class OperatorAttributeError(AttributeError):
    def __init__(self,s:T,target:str) -> None:
        message:str = exp.operator_attribute_error(s,target)
        super().__init__(message)
    
left_ops:Tuple[str,...] = tuple(operator_functions.keys())
right_ops:Tuple[str,...] = tuple(operator_fallback.keys())
inplace_ops:Tuple[str,...] = tuple(operator_inline_functions.keys())
