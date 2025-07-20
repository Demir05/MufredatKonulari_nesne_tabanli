from functools import wraps

# -------------------------------------------
# 🔍 @functools.wraps
# -------------------------------------------
# Bu dekoratör, başka bir dekoratör içinde tanımlanan wrapper fonksiyonunun
# metadata'sını (örn: __name__, __doc__, __module__) orijinal fonksiyondan kopyalar.

# NEDEN KULLANILIR?
# -----------------
# 🎯 Debugging (hata ayıklama) sırasında traceback'lerin doğru fonksiyon ismini göstermesi için
# 📚 help(), inspect gibi araçların doğru dokümantasyona ulaşabilmesi için
# 🧪 test framework’lerinin doğru şekilde çalışması için
# 🔍 introspection (örn: inspect.signature) işlemlerinin sağlıklı sonuç vermesi için
# 👨‍💻 ve kodun daha Pythonic, temiz ve anlaşılır olması için

# NE YAPAR?
# ---------
# wraps(func) çağrısı, aslında functools.update_wrapper(wrapper, func) fonksiyonunu çalıştırır.
# Bu, aşağıdaki nitelikleri 'func' fonksiyonundan alıp 'wrapper'a taşır:
# ✅ __module__
# ✅ __name__
# ✅ __qualname__
# ✅ __annotations__
# ✅ __doc__
# ✅ __dict__

# ELLE YAPILABİLİR Mİ?
# ---------------------
# Evet, örn:
#   wrapper.__name__ = func.__name__
# Ama bu eksiktir ve sıkıcıdır. Ayrıca genişletilebilir değildir.
# ❗ Bu yüzden @wraps tercih edilir.

# NEREDE KULLANILMAZ?
# -------------------
# - Eğer wrapper fonksiyonunun, orijinal fonksiyonla hiçbir ilgisi kalmayacaksa (örn: yeni bir API sarmalanıyorsa),
#   @wraps gereksiz olabilir.
# - Veya wrapper fonksiyonu tamamen farklı bir işlem yapıyorsa (örn: fonksiyonu simüle ediyorsa).

# -------------------------------------------
# ✅ KULLANIM ÖRNEĞİ:
# -------------------------------------------

def logger(func):
    @wraps(func)  # 👉 Bu satır olmazsa, wrapper'ın adı 'func' yerine 'wrapper' olur
    def wrapper(*args, **kwargs):
        print(f"[log] {func.__name__} çağrılıyor...")
        return func(*args, **kwargs)
    return wrapper

@logger
def greet(name: str) -> str:
    """Kullanıcıyı selamlar."""

    return f"Merhaba {name}"

print(greet("Aslı"))         # Merhaba Aslı
print(greet.__name__)        # greet  (wraps olmasaydı 'wrapper')
print(greet.__doc__)         # Kullanıcıyı selamlar.
print(greet.__dict__)        # {'__wrapped__': <function greet at 0x7bd7f4618ea0>}
print(greet.__annotations__ ) # {'name': <class 'str'>, 'return': <class 'str'>}
print(greet.__module__)       # __main__
print(greet.__qualname__)     # greet

def my_wrapper(func):
    attributes_assigned = ("__doc__", "__annotations__", "__module__", "__qualname__","__name__")
    attibutes_updated = ("__dict__",)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    for attr in attributes_assigned:
        setattr(wrapper, attr, getattr(func, attr))
    for attr in attibutes_updated:
        getattr(wrapper, attr).update(getattr(func, attr, {}))
    return wrapper

@my_wrapper
def deneme():
    """bbbb"""

    return


print(deneme.__name__)
print(deneme.__doc__)
print(deneme.__annotations__)
print(deneme.__module__)
print(deneme.__qualname__)
print(deneme.__dict__)