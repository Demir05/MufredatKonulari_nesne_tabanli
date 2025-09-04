
import types
from importlib import machinery
from typing import List, Optional, Union, Sequence
import os, re

PathLikeStr = Union[str, bytes]


def normalize_path(path: PathLikeStr, _abs: bool = True) -> str:
    """
    Normalize a single filesystem path.
    """
    normalized = os.path.normcase(os.path.normpath(path))
    return os.path.abspath(normalized) if _abs else normalized


def normalize_paths(paths: Sequence[PathLikeStr], _abs: bool = True) -> List[str]:
    """
    Normalize a list of paths.
    """
    return [normalize_path(path, _abs) for path in paths]


def is_real_path(__p: PathLikeStr) -> bool:
    """
    Check if path exists on filesystem.
    """
    return os.path.isfile(__p) or os.path.isdir(__p)

def find_real_path(__p: PathLikeStr, look_up_table: Sequence[PathLikeStr]) -> List[PathLikeStr]|None:

    look_up_table = normalize_paths(look_up_table,False)
    __p = normalize_path(__p, False)
    succses: List[PathLikeStr] = []

    for path in look_up_table:
        full_path = os.path.join(path,__p)

        if is_real_path(full_path):
            succses.append(full_path)
            print(succses)
    return succses if succses else None

def from_doc_name(__p: str, filex_for_dot: Optional[str] = ".py") -> PathLikeStr:
    """
    Convert dot-separated module name to full file path.
    """
    p = os.path.join(*__p.split("."))
    return p + filex_for_dot if filex_for_dot is not None else p


def get_longest_path(to_relativize_from: List[PathLikeStr], target: PathLikeStr) -> Optional[str]:
    """
    Get the longest common prefix path from a list of root paths.
    """
    best = ""
    max_len = 0
    target = normalize_path(target)
    trf = normalize_paths(to_relativize_from)
    print("target", target)
    for _path in trf:
        try:
            common = os.path.commonpath([target, _path])

            print("path",_path)
            if normalize_path(common, False) == normalize_path(_path, False) and len(common) > max_len:
                best = _path
                max_len = len(common)
        except ValueError:
            continue

    return best or None


def doc_from_path(__p: str, view_root: bool = True) -> str:
    parts = __p.split(os.sep)
    dotted = ".".join(parts)
    return dotted.lstrip("c:.") if not view_root else dotted


def from_path_name(
    __p: str,
    to_relativize_from: Optional[List[str]],
    target: Optional[str],
    view_root: bool = True
) -> Optional[str]:
    if to_relativize_from and target:
        if (relpath := get_longest_path(to_relativize_from, target)) is None:
            return None
        return doc_from_path(relpath, view_root)

    return doc_from_path(__p, view_root)


def handle_path_or_name(
    path: str,
    to_relativize_from_the_right_root: Optional[List[str]] = None,
    target_path_for_relativize: Optional[str] = None,
    filex_for_dot: str = ".py",
    view_root: bool = True,
    solid: bool = False
) -> Optional[str]:
    compiled = re.compile(r"^([a-z]+)(\.[a-z]+)*$")

    if compiled.fullmatch(path):
        result = from_doc_name(path, filex_for_dot)
        if solid and not is_real_path(result):
            raise ValueError(f"{result} is not a real path")
        return result

    path = normalize_path(path)

    if solid and not is_real_path(path):
        raise ValueError(f"{path} is not a real path")

    return from_path_name(
        __p=path,
        to_relativize_from=to_relativize_from_the_right_root,
        target=target_path_for_relativize,
        view_root=view_root
    )


def join_paths(last: str, path: str) -> str:
    if ".py" not in last:
        last += ".py"
    return os.path.join(path, last)

def re_organize_path_for_relative(__root_path: str, _head: str, extension: Optional[str] = None) -> str:
    if os.path.isabs(_head):
        _head = os.path.relpath(_head, __root_path)
    p = os.path.join(__root_path, _head)
    return p + extension if extension else p

def module_is_regular_package(module_path: str) -> bool:
    return os.path.exists(os.path.join(module_path, "__init__.py"))

def module_is_namespace_package(fullname: str, _path: List[str]) -> bool:
    names: List[str] = fullname.split(".")

    return not any(module_is_regular_package(os.path.join(root,*names)) for root in _path)

def module_namespace_get_search_locations(fullname: str,_path: List[str]) -> List[str]|None:
    if not module_is_namespace_package(fullname, _path):
        return None

    names: List[str] = fullname.split(".")
    paths: List[str] = []

    for root in _path:
        paths.append(os.path.join(root, *names))

    return paths


def configure_attributes(__o, **kwargs):
    for name, value in kwargs.items():
        setattr(__o, name, value)

def module_from_spec(spec: machinery.ModuleSpec) -> types.ModuleType|None:

    if hasattr(spec.loader, "create_module") and (cm:=getattr(spec.loader, "create_module"))(spec) is not None:
        mod = cm

    else:
        mod = types.ModuleType(spec.name)

    configure_attributes(mod,
                         __name__= spec.name,
                         __loader__= spec.loader,
                         __spec__= spec,
                         __path__ = spec.submodule_search_locations if spec.submodule_search_locations else "",
                         __package__ = spec.parent,
                         __file__ = spec.origin if spec.origin != "namespace" else None)

    return mod


def load_from_module(module: types.ModuleType) -> None:
    if hasattr(module, '__spec__') and module.__spec__ is not None:
        getattr(module.__spec__, 'loader').exec_module(module)
