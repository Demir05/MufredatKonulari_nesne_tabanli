import types


class UserAPI:

    def login(self) -> None:
        print("merhaba",self.__class__.__name__)

    def logout(self) -> None:
        print("baybay",self.__class__.__name__)


class LazyModule(types.ModuleType):

    def __getattribute__(self, name):
        if name == "user":
            return UserAPI()
        return super().__getattribute__(name)