from symtable import Class

from mypy.fastparse import Call

from constants import IMMUTABLE,ManagerExpections,operator_functions,operator_inline_functions
from typing import TypeVar, Dict, Callable, Any, Union, Generator, Optional

T = TypeVar("T")
manager_expections = ManagerExpections()

class ClasToolsComponents:
    @staticmethod
    def is_mutable(obj:T) -> bool:
        return not isinstance(obj, IMMUTABLE)

    @staticmethod
    def give_function(name,lookuptable:Dict[str,Callable[...,Any]]) -> Optional[Callable[...,Any]]:
        try:
            base_func = ClasToolsComponents.inject_from_pools(name,lookuptable)
            return base_func
        except Exception as e:
            manager_expections.exp.operator_not_found(e)
            return None


    @staticmethod
    def inject_from_pools(name,lookuptable:Dict[str,Callable[...,Any]]) -> Callable[...,Any]:
        return lookuptable[name]

    @staticmethod
    def inject_to_class(cls:type[T],ops:Union[str,tuple],func:Callable[...,Any]) -> None:
        """Bunu kullanman gerek"""
        # name -> tuple
        if isinstance(ops,str):
            ops = (ops,)

        for n in ops:
            if n in vars(cls):
                continue
            else:
                try:
                    setattr(cls,n,func)
                except  Exception as e: manager_expections.exp.inject_error(e)

    @staticmethod
    def make_method( mode:str,cls:type[T],target:str, class_args) ->Callable[[Callable[[Any, Any], Any]], Callable[[Any, Any], T]]:
        def base_wrapper(func:Callable[[Any,Any],Any]) -> Callable[[Any,Any],T]:
            def wrapper(self,other,**kwargs) -> Union[T,Any]:
                result = func(self,other,**kwargs)

                match mode:
                    case "left":
                        return cls(result, *class_args)
                    case "inplace":
                        if ClasToolsComponents.is_mutable(getattr(self, target)):
                            return cls(result, *class_args)
                        else:
                            setattr(self,target,result)
                            return self
                    case "right":
                        ...
                    case _:
                        return None
            return wrapper
        return base_wrapper


    @staticmethod
    def total_inject(cls: type[T],mode:str,lookuptable:Dict[str,Callable[...,Any]], target: str, ops: Union[str, tuple],  *class_args) -> None:
        if isinstance(ops, str):
            ops = (ops,)

        for name in ops:
            base_func = ClasToolsComponents.give_function(name,lookuptable)
            def make_func(_func):
                @ClasToolsComponents.make_method(mode,cls,target,*class_args)
                def method(self, other, __f=_func):
                    result = __f(getattr(self, target), getattr(other, target))
                    return result
                return method

            ClasToolsComponents.inject_to_class(cls, name, make_func(base_func))

class LeftHandOperators:

    @staticmethod
    def basic_operators(target:str,ops= ("__add__","__sub__","__mul__","__truediv__","__floordiv__","__pow__"), *class_args) -> Callable[[type[T]],type[T]]:
        def wrapper(cls:type[T]) -> type[T]:
            ClasToolsComponents.total_inject(cls,"left",operator_functions,target,ops,class_args)
            return cls
        return wrapper

class InplaceOperators:

    @staticmethod
    def basic_operators(target: str,*class_args,ops=("__iadd__", "__isub__", "__imul__", "__itruediv__", "__ifloordiv__", "__ipow__")) -> Callable[[type[T]], type[T]]:

        def wrapper(cls: type[T]) -> type[T]:
            ClasToolsComponents.total_inject(cls,"inplace",operator_inline_functions, target, ops,class_args)
            return cls
        return wrapper

class RightHandOperators:
    ...

@InplaceOperators.basic_operators("data")
class A:
    def __init__(self,data):
        self.data = data


a = A(1)
a1 = A(2)

a+= a1
print(a.data)