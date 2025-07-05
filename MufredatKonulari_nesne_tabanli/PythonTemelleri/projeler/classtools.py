

from constants import IMMUTABLE,ManagerExpections,OperatorAttributeError,operator_functions,operator_inline_functions,operator_fallback,left_ops,right_ops,inplace_ops
from typing import TypeVar, Dict, Callable, Any, Union, Optional, Tuple, Literal

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
            def wrapper(self,other)->Union[T,type[T],str,None]:
                result:Union[T,type[T],str] = func(self,other)

                match mode:
                    case "left":
                        return cls(result, *class_args)
                    case "inplace":

                        if ClasToolsComponents.is_mutable(getattr(self, target)):
                            setattr(self, target, result)
                            return self

                        else:
                            return cls(result, *class_args)
                    case "right":
                        return result
                return None
            return wrapper
        return base_wrapper

    @staticmethod
    def basic_operators(target: str,mode:str,ops:tuple,*class_args) -> Callable[[type[T]], type[T]]:
        def wrapper(cls:type[T]) -> type[T]:
            ClasToolsComponents.total_inject(cls, mode, operator_inline_functions, target, ops, class_args)
            return cls

        return wrapper

    @staticmethod
    def check_attribute(target:str,self:Any,other:Any) -> bool:
       if hasattr(self,target):
           return True if hasattr(other,target) else False
       raise OperatorAttributeError(self,target)

    @staticmethod
    def total_inject(cls: type[T],mode:str,lookuptable:Dict[str,Callable[...,Any]], target: str, ops: Union[str, tuple],  *class_args) -> None:
        if isinstance(ops, str):
            ops = (ops,)

        for name in ops:
            base_func = ClasToolsComponents.give_function(name,lookuptable)
            def make_func(_func) -> Callable[...,Union[T,type[T],str]]:
                @ClasToolsComponents.make_method(mode,cls,target,*class_args)
                def method(self, other, __f=_func) -> Union[T,type[T],str]:
                    if ClasToolsComponents.check_attribute(target,self,other):
                        result:Union[T,type[T],str] = __f(getattr(self, target), getattr(other, target))
                    else:
                        result = __f(self,other)
                    return result
                return method

            ClasToolsComponents.inject_to_class(cls, name, make_func(base_func))

class InjectOperators:
   def __init__(self,target: str,mode:Literal["left","inplace","right"],*class_args) -> None:
       self.target:str = target
       self.mode:str = mode
       self.class_args = class_args
       self.ops:Union[Tuple[str,...]] = self.change_ops(mode)

   def change_ops(self,mode:str) -> Tuple[str,...]:
        if self.ops is None:
            self.ops = left_ops if mode =="left" else inplace_ops if mode =="inplace" else right_ops
        return self.ops

   def __call__(self,cls:type[T]) -> type[T]:
        match self.mode:
            case "left":

                ClasToolsComponents.total_inject(cls, self.mode, operator_functions, self.target,  self.ops, self.class_args)
            case "inplace":

                ClasToolsComponents.total_inject(cls, self.mode, operator_inline_functions, self.target, self.ops, self.class_args)
            case "right":

                ClasToolsComponents.total_inject(cls, self.mode, operator_fallback, self.target, self.ops, self.class_args)
        return cls



