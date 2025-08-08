
from collections import defaultdict
from inspect import *

from mypy.literals import literal

from exeptionmanager import *
from errors import *

def check(_arg: Any, expected_type: type) -> None:

    if not type_check(_arg, expected_type):
        raise TypeError(CUSTOM_USER_MESSAGE(f"{_arg} is not {expected_type}"))

def is_type_match(value: Any, expected: Any) -> bool:
    origin = get_origin(expected)
    _args = get_args(expected)

    if origin is Union:
        return any(isinstance(value, t) for t in _args)
    else:
        return isinstance(value, expected)



validate_collections = lambda _value, _args, _origin: all_match_type(_value, _args) and isinstance(_value, _origin)



# Özel validator eşlemeleri
specials = {
    Union: any,
    Optional: any,
    Literal: all,
}

def all_match_type(values: Any, expected_types: Any) -> bool:
    if not isinstance(values, Iterable) or isinstance(values, (str, bytes)):
        return False
    return len(values) == len(expected_types) and all(isinstance(v, t) for v, t in zip(values, expected_types))

def dict_match_type(values: Dict, expected_types) -> bool:
    ktype, vtype = expected_types
    return all(isinstance(k, ktype) and isinstance(v, vtype) for k, v in values.items())

def iscollection(_args: Tuple[Any, ...]) -> bool:
    return all(arg not in specials for arg in _args)

def type_check(value: Any, expected_type: Any) -> bool:
    """
       Recursively validates whether a given value matches the specified typing annotation.

       This function supports a wide range of complex typing constructs, including:
       - Union, Optional, Literal
       - List, Tuple, Dict
       - Nested and recursive combinations (e.g., Union[Tuple[str, int], Dict[str, str]])
       - Variadic Tuples (Tuple[int, ...])

       Parameters:
           value (Any): The actual runtime value to be validated.
           expected_type (Any): A PEP 484-style typing hint to validate against.

       Returns:
           bool: True if the value conforms to the expected type annotation, False otherwise.

       Examples:
           >>> type_check(10, int)
           True
           >>> type_check({"name": "demir"}, Dict[str, str])
           True
           >>> type_check(["hello"], Union[List[str], int])
           True
           >>> type_check(("a", "b"), Tuple[str, str])
           True
           >>> type_check("guest", Literal["admin", "user"])
           False

       Notes:
           This function acts as the engine behind higher-level decorators like `@signcheck`
           and `@returncheck`, enabling runtime type enforcement based on static annotations.

       Limitations:
           - Custom Generic types or forward references are not fully supported.
           - Literal and Optional types are matched by value, not by semantics.
       """
    origin = get_origin(expected_type)
    args = get_args(expected_type)

    if isinstance(origin, type) and iscollection(args):
        return dict_match_type(value, args) if origin is dict else all_match_type(value, args)

    def type_chain(_expected_type: Any, _value: Any = None, branch_id: int = 0) -> Generator[Tuple[bool, Callable, int], None, None]:
        _origin = get_origin(_expected_type)
        _args = get_args(_expected_type)

        if _origin in specials:
            _validator = specials[_origin]
            for i, arg in enumerate(_args):
                yield from type_chain(arg, _value, i)
            yield True, _validator, -1

        elif _origin in {list,tuple}:
            if not isinstance(_value, Iterable) or isinstance(_value, (str, bytes)):
                yield False, all, branch_id
            elif len(_args) == 2 and _args[1] is Ellipsis:
                yield all(isinstance(v, _args[0]) for v in _value), all, branch_id
            else:
                yield all_match_type(_value, _args), all, branch_id

        elif _origin is dict:
            yield dict_match_type(_value, _args), all, branch_id

        elif _origin is literal:
            yield _value in _args, all, branch_id

        else:
            yield isinstance(_value, _expected_type), all, branch_id

    buckets = defaultdict(list)
    for result, validator, bid in type_chain(expected_type, value):
        if bid != -1:
            buckets[(validator, bid)].append(result)

    results = [
        validator(results) if validator in {all, any} else False
        for (validator, _), results in buckets.items()
    ]


    return any(results)


class FuncTools:

    @staticmethod
    def returncheck(func: Callable) -> Callable:
        """
        A decorator that enforces runtime type-checking for the return value of a function.

        If the function has a return type annotation, it validates that the actual return
        value matches the expected type using `check()` / `is_type_match()`.

        Raises:
            TypeError: If the return value doesn't match the declared type
        """

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            sig = signature(func)
            returnType = sig.return_annotation
            result = func(*args, **kwargs)
            if returnType is not Signature.empty:
                check(result, returnType)

            return result

        return wrapper

    @staticmethod
    def signcheck(func: Callable) -> Callable:
        """
            A runtime signature-checking decorator for validating function arguments against type hints.

            This decorator intercepts function calls and verifies that all provided positional,
            keyword, variadic (*args), and keyword variadic (**kwargs) arguments conform to the
            type annotations defined in the function signature.

            Features:
            - Supports basic types (int, str, etc.)
            - Handles container types: tuple, dict, etc.
            - Supports typing hints like Union, Optional, Literal, etc.
            - Recursive unpacking of arguments for deep validation
            - Raises TypeError on first type mismatch with a descriptive message

            Example:
                @signcheck
                def greet(name: str, age: int, *tags: Union[str, int], **kwargs: str):
                    ...

                greet("Alice", 30, "engineer", 99, city="Berlin")
                # Works

                greet("Alice", "not-a-number")
                # Raises TypeError: 'not-a-number' is not <class 'int'>

            Returns:
                A wrapped function that enforces type validation before execution.
            """

        if not isfunction(func):
            raise UserError(FIELD_NOT_CALLABLE)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            def return_arguments_params() -> Tuple[List[type], List[ValuesView]]:

                sig = signature(func)
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()

                type_hints: List[type] = [param.annotation for param in sig.parameters.values()]
                argument_values: List[Any] = list(bound.arguments.values())

                return type_hints, argument_values

            def validate() -> None:
                typeHints, argument_values = return_arguments_params()

                for typeHint, argument in zip(typeHints, argument_values):

                    match argument:

                        case tuple():
                            for _arg in argument:
                                check(_arg, typeHint)
                        case dict():
                            for _arg in argument.values():
                                check(_arg, typeHint)
                        case _:
                            check(argument, typeHint)

            validate()
            return FuncTools.returncheck(func)

        return wrapper


