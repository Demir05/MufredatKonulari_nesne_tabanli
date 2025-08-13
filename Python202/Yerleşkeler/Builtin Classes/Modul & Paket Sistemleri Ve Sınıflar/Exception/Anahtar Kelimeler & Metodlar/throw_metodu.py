# ============================================================
# 📌 Python’da throw — Full Detaylı, Sade Açıklama
# ============================================================

# ------------------------------------------------------------
# 1️⃣ "throw" kelimesi günlük dilde ne anlama gelir?
# ------------------------------------------------------------
# - Java, C#, JavaScript gibi dillerde "throw" → exception fırlatmak.
# - Python’da bunun karşılığı `raise` anahtar kelimesidir.
# - Yani "throw an exception" dediğinde Python’da "raise an exception" dersin.

# ÖRNEK (Java mantığı Python’a çevrilmiş):
# Java: throw new ValueError("mesaj");
# Python: raise ValueError("mesaj")

# ------------------------------------------------------------
# 2️⃣ Teknik olarak Python'da throw metodu nerede var?
# ------------------------------------------------------------
# - "throw" isimli bir **method**, Python’un **generator** (ve coroutine) objelerinde vardır.
# - Amacı: Generator çalışırken, içine dışarıdan bir exception “fırlatmak”.
# - Böylece generator’un normal akışını kesip, içeride exception handling başlatabilirsin.

# ------------------------------------------------------------
# 3️⃣ generator.throw nasıl çalışır?
# ------------------------------------------------------------
# Yapı:
#   generator.throw(exc_type, exc_value=None, traceback=None)
# Parametreler:
#   exc_type  → fırlatılacak hata tipi (ValueError, RuntimeError vs.)
#   exc_value → hata mesajı veya exception nesnesi (opsiyonel)
#   traceback → özel traceback objesi (çok nadir kullanılır)
#
# Çalışma:
# - generator bekleyen yield noktasına döner.
# - Orada normal veri dönmek yerine exception fırlatılır.
# - Eğer generator içinde try/except varsa, o hata yakalanabilir.
# - Yakalanmazsa generator sonlanır ve hata üst katmana çıkar.

# ------------------------------------------------------------
# 4️⃣ Pratik Örnek: generator.throw
# ------------------------------------------------------------
def my_gen():
    try:
        yield 1
        yield 2
    except ValueError as e:
        print("Generator içinde hata yakalandı:", e)
        yield "recovered"  # hata sonrası toparlanma
    yield 3

g = my_gen()
print(next(g))                # 1
print(g.throw(ValueError, "test hatası"))  # throw ile hata fırlatılır, içeride yakalanır
print(next(g))                # 3

# ÇIKTI:
# 1
# Generator içinde hata yakalandı: test hatası
# recovered
# 3

# ------------------------------------------------------------
# 5️⃣ throw ve raise farkı
# ------------------------------------------------------------
# - raise: bulunduğun scope’ta hemen exception fırlatır.
# - throw: çalışmakta olan generator’un içine dışarıdan exception fırlatır.
# - Yani throw, bir **generator kontrol metodudur**, raise ise genel exception mekanizması.

# ------------------------------------------------------------
# 6️⃣ Nerede kullanılır?
# ------------------------------------------------------------
# - Asenkron veri akışlarında (pipelines)
# - Coroutine tabanlı durum makinelerinde
# - Generator ile çalışan stateful iş akışlarında “erken hata” göndermek için
#
# Çoğu Python programcısı günlük hayatta throw kullanmaz,
# ama advanced async / generator bazlı framework’lerde (ör. asyncio, Trio) sık sık geçer.


# ============================================================
# DEMO 2 — throw: yakalanmazsa hata DIŞARI taşar ve generator biter
# ============================================================

def gen_no_catch():
    yield "A"
    yield "B"
    # burada ValueError yakalanmıyor → dışarı taşacak
    yield "C"

g = gen_no_catch()
print(next(g))                  # → "A"
try:
    # ValueError içerde yakalanmadığı için dışarı fırlar
    g.throw(ValueError, "unhandled")
except ValueError as e:
    print("[main] dışarıda yakalandı:", e)

# Unutma: unhandled throw generator'ı genellikle SONLANDIRIR.
# Çoğu durumda artık next(g) → StopIteration olur.
try:
    print(next(g))
except StopIteration:
    print("[main] generator kapandı (throw sonrası)")



# ============================================================
# DEMO 3 — close(): GeneratorExit fırlatır, farkı nedir?
# ============================================================
# .close(), generator'ın içine "GeneratorExit" fırlatır.
# Bu, "kapanıyorsun, temizliğini yap" sinyalidir.
# Not: GeneratorExit *yakalanmamalı*; yakalarsan DERHAL yeniden raise etmelisin.
# Aksi halde Python, RuntimeError yükseltir.

def gen_with_cleanup():
    try:
        print("[gen] acquire resource")
        while True:
            yield "tick"
    except GeneratorExit:
        print("[gen] cleanup on close()")  # burada dosya/soket/lock kapatılır
        # raise  ← normalde tekrar raise etmene gerek yok; return da edebilirsin
    finally:
        print("[gen] finally always runs")

g = gen_with_cleanup()
print(next(g))                   # → "tick"
g.close()                        # → GeneratorExit içeri atılır
print("[main] closed, further next() will StopIteration")
try:
    print(next(g))
except StopIteration:
    print("[main] generator is done")


# ============================================================
# DEMO 4 — send vs throw vs close (yan yana mini özet)
# ============================================================

def mini():
    try:
        x = yield "ready"                # 1) ilk yield
        yield f"got: {x}"                # 2) send ile değer verilebilir
    except RuntimeError as e:            # 3) throw RuntimeError olursa buraya düşer
        yield f"handled: {e}"            # 4) toparlanıp değer döndürebilir
    finally:
        print("[mini] finally cleanup")  # 5) her durumda çalışır

g = mini()
print(next(g))                # → "ready"
print(g.send("DATA"))         # → "got: DATA"
print(g.throw(RuntimeError, "uh-oh"))  # → "handled: uh-oh"
try:
    g.close()                 # → GeneratorExit (cleanup)
except RuntimeError:
    pass
