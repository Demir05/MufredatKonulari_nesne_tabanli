import types


def reload_module(module: types.ModuleType):
    module.__spec__.loader.exec_module(module)


