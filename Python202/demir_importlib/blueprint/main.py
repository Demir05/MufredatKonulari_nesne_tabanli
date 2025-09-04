
__dir__ = ['user']

def main():
    from .bluep import LazyModule as LM
    import sys

    sys.modules[__name__] = LM(__name__)


if __name__ != "__main__":


    if __import__("typing",fromlist=["TYPE_CHECKING"]).TYPE_CHECKING :
        from .bluep import UserAPI
        user: UserAPI

    main()

