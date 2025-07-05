# ---------------------------------------
# 📌 Dinamik Decorator Kullanımı
# ---------------------------------------
# Python'da @decorator ifadesi aslında:
#    decorated_func = decorator(original_func)
# anlamına gelir.
# "decorator" burada fonksiyon, sınıf ya da callable bir nesne olabilir.
# @ işareti sadece bir çağrıyı tetikler: decorator(func)
# Dolayısıyla decorator ifadesi, runtime'da dinamik olarak atanabilir.

# ---------------------------------------
# 🧠 Fonksiyonel decorator örnekleri
# ---------------------------------------

def log(func):
    def wrapper(*args, **kwargs):
        print(f"{func.__name__} çağrıldı.")
        return func(*args, **kwargs)
    return wrapper

def noop(func):
    # hiçbir şey yapmayan decorator
    return func

# Koşula bağlı decorator seçimi (runtime)
debug = True
dec = log if debug else noop

@dec
def selamla():
    print("Merhaba!")

selamla()

# ---------------------------------------
# 🧠 Sınıf tabanlı decorator örnekleri
# ---------------------------------------

class Logger:
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f"[{self.prefix}] {func.__name__} çağrıldı.")
            return func(*args, **kwargs)
        return wrapper

class NoOp:
    def __call__(self, func):
        # hiçbir değişiklik yapmadan fonksiyonu döndürür
        return func

# Sınıf bazlı decorator'larda da dinamik atama yapılabilir:
mode = "DEBUG"

dec = Logger(mode) if mode == "DEBUG" else NoOp()

@dec
def yükle():
    print("Veri yüklendi")

yükle()

# ---------------------------------------
# 🎛️ Parametreli sınıf decorator ve runtime seçimi
# ---------------------------------------
# Sınıf decorator'lar da birer callable nesne oldukları sürece,
# her türlü dinamik seçimde kullanılabilir.
# Kullanılan nesne sadece __call__ metodunu içermelidir.

# ---------------------------------------
# 🧩 Sonuç:
# Hem fonksiyonel hem de sınıf bazlı decorator’larda,
# @dec kullanımı aslında sadece "dec(func)" çağrısıdır.
# dec ifadesi runtime'da herhangi bir değer olabilir:
# bir fonksiyon, bir sınıf örneği, ya da bir factory fonksiyonu sonucu.

# Bu özellik, Python’da yüksek esneklikli, yapılandırılabilir sistemler tasarlamayı mümkün kılar.