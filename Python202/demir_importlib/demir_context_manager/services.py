from __future__ import annotations
from inspect import isclass
from typing import Tuple, Dict, Any, List, Optional, Type, Callable, Generator
import types
from demir_importlib.demir_exception import demir_exception

class MetaValidate(type):
    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        attrs: Dict[str, Any],
        **kwargs: Any,
    ) -> type:
        # kontrol et
        if (attrs.get("__enter__") and attrs.get("__exit__")) is None:
            raise NotImplementedError("__enter__ or __exit__ must be implemented")

        return type.__new__(cls, name, bases, attrs, **kwargs)


class InjectSlots(MetaValidate):
    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        attrs: Dict[str, Any],
        **kwargs: Any,
    ) -> type:
        # slots tanımlı mı ?
        if not attrs.get("__slots__"):

            def inheritance_control(_bases: Tuple[type, ...]) -> bool:
                return all("__slots__" not in vars(base_cls) for base_cls in _bases)

            def inject_slots(_cls: type) -> None:
                assert "__slots__" not in vars(_cls), "Sınıfta zaten slots tanımlı"
                setattr(_cls, "__slots__", tuple(m for m in get_possible_members(_cls)))

            # öncelikle kimler slot içinde olcak bul
            def get_possible_members(look_up: type | Dict[str, Any]) -> Tuple[str, ...]:
                annotations_members: List[str] = []
                static_attributes_members: List[str] = []

                if isclass(look_up):
                    look_up = vars(look_up)
                elif not isinstance(look_up, dict):
                    raise TypeError("'look_up' must be a type or a dictionary")

                # annotations kontrolü
                annotations_members[::] = [
                    member
                    for member in look_up.get("__annotations__", [])
                    if member not in look_up
                ]
                # static attributs kontrol et
                if static_attributes := look_up.get("__static_attributes__"):
                    static_attributes_members[::] = [attribute for attribute in static_attributes]

                return tuple(m for m in annotations_members + static_attributes_members)

            attrs["__slots__"] = get_possible_members(attrs)

        return super().__new__(cls, name, bases, attrs, **kwargs)


class Traceio(metaclass=InjectSlots):


    def __enter__(self) -> "Traceio":
          # type: ignore
        self.demir_exception = demir_exception
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> bool:
        if exc_type and exc_val:
            # tipli çağrılar; demir_exception API'si Any olduğu için local türler Any
            tracebacks: List[types.TracebackType | None] = self.demir_exception.collect_tracebacks(exc_val)  # type: ignore[attr-defined]
            nps: List[Any] = self.demir_exception.get_frame_attributes(tracebacks)  # type: ignore[attr-defined]

            from pprint import pprint

            for np in nps:
                pprint(self.demir_exception.deep_namedtuple_dict(np))  # type: ignore[attr-defined]

        return True


def contextmanager(func: Callable[[Any],Generator[Any,None,None]]) -> type:

    class ContextManager(Traceio):

        def __init__(self, *args, **kwargs):
            self.gen = func(*args, **kwargs)

        def __enter__(self):
            super().__enter__()
            return next(self.gen)

        def __exit__(self, exc_type, exc_val, exc_tb):
            result = super().__exit__(exc_type, exc_val, exc_tb)
            if exc_type:
                try:
                    self.gen.throw(exc_val)
                except StopIteration:
                    return result
                else:
                    return False

            try:
                return next(self.gen)
            except StopIteration:
                return False
    return ContextManager




