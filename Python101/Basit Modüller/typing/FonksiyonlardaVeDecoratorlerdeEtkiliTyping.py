# ─────────────────────────────────────────────────────────────
# 📘 BAŞLIK: "Fonksiyonlarda ve Dekoratörlerde Etkili Typing Stratejileri"
# ─────────────────────────────────────────────────────────────
# 🔍 Bu rehber, birden fazla fonksiyonun birbiriyle ilişkili olduğu durumlarda
# hangi parametrelerin `TypeVar` ile, hangilerinin sabit tiplerle tanımlanması
# gerektiğini açıklar.
# Amaç: Type Hinting'i doğru, anlaşılır ve minimal karmaşıklıkla yapabilmek.
# ─────────────────────────────────────────────────────────────

from typing import TypeVar, Callable, Optional, Iterator, Any

# ─────────────────────────────────────────────
# 🧩 1. TypeVar NEDİR? Ne zaman kullanılır?
# ─────────────────────────────────────────────
# `TypeVar` (tip değişkeni) sayesinde fonksiyonlar, sınıflar veya dekoratörler,
# belirli bir türle çalışmak yerine herhangi bir türle çalışabilir hale getirilir.
# Genellikle fonksiyonlar/sınıflar birbirine bağlıysa ve aynı türü paylaşması gerekiyorsa kullanılır.

T = TypeVar("T")  # Genel tip değişkeni (her tür olabilir)

# ─────────────────────────────────────────────
# ✅ NEDEN `T` kullanıyoruz?
# ─────────────────────────────────────────────
# Çünkü `cls` parametresi (bir sınıf), her fonksiyonda kullanılacak.
# `check_iter`, `inject_methods`, `wrapper` hepsi bu `cls`'yi işler.
# Bu sınıfın tipi korunmalı ve ortak olmalı.

# ─────────────────────────────────────────────
# ❌ NEDEN `str`, `bool` için `TypeVar` kullanmıyoruz?
# ─────────────────────────────────────────────
# Çünkü bu parametreler dinamik değil, sabittir:
# `target: str`  → daima string olacak ("data", "items", "info"...)
# `is_iter: bool` → sadece `True` ya da `False` alacak.
# Yani buradaki türler sabit olduğu için `TypeVar` kullanmak gereksiz ve kafa karıştırıcıdır.

# ─────────────────────────────────────────────
# ⚠️ "Ama `Callable[..., Any]` neden kullanılıyor?"
# ─────────────────────────────────────────────
# Çünkü `Callable[[T], Iterator[Any]]` gibi karmaşık tiplerin, `setattr()` gibi
# dinamik işlerde doğrulanmasının anlamı yoktur.
# O yüzden çoğu zaman:
# → `Callable[..., Any]` yeterlidir. Daha sade ve uyumludur.

# ─────────────────────────────────────────────
# 🧠 Gelişmiş Not:
# Eğer farklı fonksiyonlar aynı `target` veya `is_iter` değerini paylaşıyorsa,
# bu değerleri `TypeVar` ile değil, doğrudan `str` ve `bool` olarak bırakmak daha doğrudur.
# Çünkü biz "tip uyumluluğu" değil, sadece sabit değer geçiriyoruz.

# ─────────────────────────────────────────────
# ✅ Fonksiyonlar birbirine tip açısından bağımlıysa → `TypeVar` kullanılır.
# ❌ Fonksiyonlar aynı literal türü (str, bool) kullanıyorsa → Gerek yok.
# ─────────────────────────────────────────────

# SONUC: Fonksiyonlar birbirlerine tip açısından bağımlıysa ortada tip uyumluğu varolup dolasıyla da tipin korunması ve ortak olması sözkonusudur
#   - bu durumda TypeVar() kullanılmalı çünkü sınıflar,Generic'dir yani herangi bir sınıf olabilirler
# Ama tipler sabit değerler olup değişmeyeceklerse
#   - burda TypeVar() kullanılması gereksiz olur ve kodu karmaşıklaştırır çünkü sabit değer geçiriyoruz

# 🧪 Örnek kullanımı:
def inject_methods(cls: type[T], name: str, func: Callable[..., Any]) -> Optional[T]:
    if name not in vars(cls):
        setattr(cls, name, func)
        return None
    return cls

def check_iter(cls: type[T], target: str, is_iter: bool) -> None:
    a: Callable[[T], Iterator[Any]] = lambda self: iter(getattr(self, target))
    b: Callable[[T], Any] = lambda self: getattr(self, target)
    functions = {
        True: b,
        False: a
    }
    inject_methods(cls, "__iter__", functions.get(is_iter, a))

def total_container(target: str, /, *, is_iter: bool = False) -> Callable[[type[T]], type[T]]:
    def wrapper(cls: type[T]) -> type[T]:
        check_iter(cls, target, is_iter)
        return cls
    return wrapper

@total_container("data")
class Deneme:
    def __init__(self, data):
        self.data = data

# 🔚
# Bu örnekte:
# - Sınıflar generic (her tür olabilir) → TypeVar kullanıldı
# - Parametreler sabit (`str`, `bool`) → doğrudan yazıldı

# Artık doğru tip kullanımıyla güçlü ve doğru yazılmış bir dekoratöre sahibiz.
