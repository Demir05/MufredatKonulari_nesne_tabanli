
from demir_importlib.app import my_machinery as mac
from demir_importlib.app import utils
from demir_importlib.app import my_importlib

spec = mac.FileFinder(r"C:\Users\demir\OneDrive\Desktop\MufredatKonulari_nesne_tabanli\MufredatKonulari_nesne_tabanli\PythonTemelleri\projeler\demir_importlib\t").find_spec("t2")

mod = utils.module_from_spec(spec)
utils.load_from_module(mod)


print(mod.a)

input()
my_importlib.reload_module(mod)
print(mod.a)