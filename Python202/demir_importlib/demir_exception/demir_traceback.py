import types
from typing import Any, Dict, List, Literal, Set, Optional
import sys

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
    assert isinstance(tb,(types.NoneType,types.TracebackType)), f"tb must be TracebackType or None got {tb}"
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


def collect_tracebacks(__e: BaseException) -> List[types.TracebackType|None]:
    """Return traceback nodes list for given exception (innermost first)."""
    return walk_traceback_nodes(getattr(__e, "__traceback__"))

def get_frame_attributes(__t: List[types.TracebackType|None]):
    """_summary_

    Args:
        __t (types.TracebackType): _description_
    """
    
    def generate_keyname(tracebacktype_object: types.TracebackType) -> str:
        assert isinstance(tracebacktype_object,types.TracebackType), f"tracebacktype_object must be TracebackType instance got {tracebacktype_object}"
        return f"{tracebacktype_object.tb_frame}.{tracebacktype_object.tb_frame.f_code.co_qualname}"
    
    buffer: Dict[str,Dict[str,Any]] = {}

    
    

if __name__ == "__main__":
    def f():
        10 / 0

    def f1():
        f()

    def f2():
        f1()

    try:
        f2()
    except ArithmeticError as a:
        tbs = collect_tracebacks(a)
        for i, tb in enumerate(tbs):
            print(i, tb.tb_frame.f_code.co_name, "line", tb.tb_lineno)