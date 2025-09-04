
import sys
from importlib import machinery
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import List, Callable, Any, TypeVar
import functools
from demir_importlib.app import utils

C = TypeVar('C',bound = Callable[...,str])

class FileFinder:

    def __init__(self, root: str)-> None:
        self.__root = utils.normalize_path(root)

    @staticmethod
    def inject_spec(func: C) -> Callable[[Any, str], ModuleSpec | None]:

        import os

        @functools.wraps(func)
        def wrapper(self: Any, fullname: str) -> ModuleSpec | None:
            fullpath = func(self, fullname)

            is_package: bool = False
            origin: str | None = None
            path: str | None = None
            has_location: bool = False
            submodule_search_locations: List[str] | None = None

            # dosya kontrolü
            if os.path.exists(__path := fullpath(".py")):
                origin = __path
                has_location = True

            elif os.path.exists(__path := fullpath()):
                is_package = True
                origin = path if utils.module_is_regular_package(
                    __path) else "namespace" if utils.module_is_namespace_package(__path, sys.path) else None

                # origin check
                if origin is None:
                    return None

                if origin != "namespace":
                    has_location = True
                    submodule_search_locations = __path

                else:
                    has_location = False
                    submodule_search_locations = utils.module_namespace_get_search_locations(fullname, sys.path)


            spec = machinery.ModuleSpec(fullname,FieldLoader(__path), origin=origin,
                                        is_package=is_package)

            # spec davranış enjeksiyonu

            utils.configure_attributes(spec,submodule_search_locations = submodule_search_locations,
            has_location = has_location,
            is_package = is_package )

            return spec

        return wrapper

    @inject_spec
    def find_spec(self, fullname: str) -> C:

        return  lambda ex = None: utils.re_organize_path_for_relative(self.__root, utils.from_doc_name(fullname, ex))

class FieldLoader:
    def __init__(self, filepath):
        self.__filepath = filepath

    def exec_module(self, module: ModuleType) -> None:
        try:
            file = open(self.__filepath, mode="r", encoding="utf-8")
        except PermissionError as e:
            raise RuntimeError from e

        except FileNotFoundError:
            return

        else:
            comp = compile(file.read(),self.__filepath, mode="exec")
            try:
                exec(comp, module.__dict__)
            except ImportError as e:
                raise RuntimeError from e
            finally:
                file.close()



