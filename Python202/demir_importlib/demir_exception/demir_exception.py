from __future__ import annotations
import types
from typing import List, Literal, Set, Optional, Any
import sys


from collections import namedtuple

MetaGroup = namedtuple("MetaGroup",["f_code",
                                        "f_locals",
                                        "f_lineo",
                                        "f_trace",
                                        ]
                           )
TraceGroup = namedtuple("TraceGroup",["keyname","meta_group"])

def walk_exception_chain(
        origin: BaseException,
        kind: Literal["cause", "context"] = "cause",
        max_depth: int = 50,
) -> List[BaseException]:
    """Walk __cause__ or __context__ chain and return list (closest first)."""
    assert isinstance(origin, BaseException), "origin must be BaseException instance"
    seen: Set[int] = set()
    buffer: List[BaseException] = []
    attr = "__" + kind + "__"
    target: Optional[BaseException] = getattr(origin, attr, None)
    depth = 0
    while target is not None and id(target) not in seen and depth < max_depth:
        seen.add(id(target))
        buffer.append(target)
        target = getattr(target, attr, None)
        depth += 1
    return buffer


def walk_traceback_nodes(tb: Optional[types.TracebackType], max_depth: int = 50) -> List[Optional[types.TracebackType]]:
    """Walk tb -> tb.tb_next linked list and return list (innermost first)."""
    assert isinstance(tb, (types.NoneType, types.TracebackType)), f"tb must be TracebackType or None got {tb}"
    buffer: List[types.TracebackType] = []
    if tb is None:
        return buffer
    seen: Set[int] = set()
    node = tb
    depth = 0
    while node is not None and id(node) not in seen and depth < max_depth:
        seen.add(id(node))
        buffer.append(node)
        node = node.tb_next
        depth += 1
    return buffer


def collect_exceptions(__e: Optional[BaseException] = None) -> List[BaseException]:
    """
    Collect exception chain for logging/reporting.

    Strategy:
      - Prefer explicit __cause__ chain (raise ... from ...).
      - If no cause, and __suppress_context__ is False, collect __context__ chain.
      - Always return a list starting with the original exception.
    """
    if __e is None:
        exception = sys.exc_info()[1]
        if exception is None:
            return []
    else:
        exception = __e

    result: List[BaseException] = [exception]

    causes = walk_exception_chain(exception, "cause")
    if causes:
        result.extend(causes)
        return result

    if not getattr(exception, "__suppress_context__", False):
        contexts = walk_exception_chain(exception, "context")
        if contexts:
            result.extend(contexts)

    return result


def collect_tracebacks(__e: BaseException) -> List[types.TracebackType | None]:
    """Return traceback nodes list for given exception (innermost first)."""
    return walk_traceback_nodes(getattr(__e, "__traceback__"))


def get_frame_attributes(__t: List[types.TracebackType | None]) -> List[TraceGroup[str,MetaGroup[Any]]|None]:
    """_summary_

    Args:
        __t (types.TracebackType): _description_
    """

    def generate_keyname(tracebacktype_object: types.TracebackType) -> str:

        import os

        assert isinstance(tracebacktype_object,
                          types.TracebackType), f"tracebacktype_object must be TracebackType instance got {tracebacktype_object}"
        return f"{os.path.normpath(os.path.normcase(tracebacktype_object.tb_frame.f_code.co_filename))}.{tracebacktype_object.tb_frame.f_code.co_qualname}"


    def filter_locals(locals_dict):
        return {k: v for k, v in locals_dict.items() if not isinstance(v, types.ModuleType)}

    def better_code(code: types.CodeType) -> str:
        return (
            f"Function: {code.co_name}\n"
            f"File: {code.co_filename}\n"
            f"Starts at line: {code.co_firstlineno}\n"
            f"Arg count: {code.co_argcount}, Locals: {code.co_nlocals}, Stack size: {code.co_stacksize}"
        )


    buffer: List[TraceGroup[str,MetaGroup[Any]]|None] = []

    for trace in __t:
        if trace is None:
            continue

        buffer.append(
            TraceGroup(
                generate_keyname(trace),MetaGroup(
                    f_code= better_code(trace.tb_frame.f_code),
                    f_locals=filter_locals(trace.tb_frame.f_locals),
                    f_lineo= trace.tb_frame.f_lineno,
                    f_trace= trace.tb_frame.f_trace,
                )
            )
        )
    return buffer

from typing import NamedTuple, Dict, Any

def deep_namedtuple_dict(nt: NamedTuple) -> Dict[str, Any]:
    assert hasattr(nt, "_fields"), "Input must be a NamedTuple"
    result: Dict[str, Any] = {}

    for field in nt._fields:
        value = getattr(nt, field)
        if hasattr(value, "_fields"):  # Nested NamedTuple
            nested = deep_namedtuple_dict(value)
            # Alan adlarını birleştirerek düzleştiriyoruz
            for k, v in nested.items():
                result[f"{field}.{k}"] = v
        else:
            result[field] = value

    return result



class DemirException(BaseException):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.__post_init__()

    def __post_init__(self):
        import sys
        self.debug_data = get_frame_attributes(collect_tracebacks(sys.exc_info()[1]))


if __name__ == "__main__":
    def f():
        raise ValueError


    def f1():
        f()


    def f2():
        f1()


    try:
        f2()
    except ValueError as a:
        try:
            raise DemirException("DemirException hatası zoooooort")
        except DemirException as b:
            print(b.debug_data)


