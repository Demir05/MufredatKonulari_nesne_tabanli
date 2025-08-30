# ============================================================
# 📌 __context__ Attribute — Tanım ve Detaylar
# ============================================================

# ------------------------------------------------------------
# 1️⃣ Nedir?
# ------------------------------------------------------------
# - Bir exception instance’ının __context__ attribute’u,
#   bu exception fırlatılmadan hemen önce *aktif olan* başka bir exception
#   varsa, ona referans tutar.
#
# - Yani "şu hata sırasında bu başka hata oluştu" bilgisini saklar.
# - Türü: Exception veya None
#
# ------------------------------------------------------------
# 2️⃣ Nasıl oluşur?
# ------------------------------------------------------------
# - Bir exception handler (except bloğu) içinde başka bir exception raise edilirse
#   Python, yeni exception’ın __context__ alanına önceki exception’ı otomatik koyar.
#
# - Bu durum **raise from** kullanılmadığında olur.
# - Eğer `raise ... from ...` kullanılırsa __context__ yerine __cause__ set edilir.
#
# ------------------------------------------------------------
# 3️⃣ Kullanım Alanları
# ------------------------------------------------------------
# ✔ Exception zincirleme → Hata akışını anlamak.
# ✔ Debugging → Asıl hatanın neden oluştuğunu geriye doğru takip etmek.
# ✔ Loglama → Önceki ve sonraki hataları birlikte kaydetmek.
#
#------------------------------------------------------------
# 🧠 Akılda Kalır
#------------------------------------------------------------
# __context__,exception zincirinin her daim korunmasını sağlayan.
# özellikle yeni kullanıcılar için hayat kurtarıcı olan bir attribute'dur
# ama amacımız excepiton chain kurmaksa raise ... from ... kullanmak çok az bir maaliyet bedeliyle
# test edilebilir,loglanabilir,soyutlanabilir,anlamlı hata çıktıları için bedelsiz bir fırsattır.
#.
# sonuç olarak kasıtlı olarak exception chain ile uğraşmamak için bir şey yapmana gerek yok python,senin yerine __context__ tutar.
# ama __cause__ ile tam bir zincir kurabilceğini ve bunun üzerinde tam kontrol sahibi olduğunu unutma.
#
#------------------------------------------------------------
# 📒 Geliştirici Notu
#------------------------------------------------------------
# Cpython'da __context__ attribute'u, bir exception fırlatırlırken hemen başka bir exception aktif olmuşşa otomatik olarak set edilir
# bunun nedeni __context__, bir hata fırlatırmak üzere başka bir hata alındığında ve bu hata, eski hatanın yerini aldığında hata geçmişini korumak amacıyla tasarlandı
# bu durum sadece bir exception aktif iken yani except bloğu içersindeyse gerçekleşir(zaten exception'ın aktif olması except bloğunana girirmiş olmasını gösterir)
# ama bağımsız olarak raise edildiğinde aktif olan başka bir exception yoktur bu nedenle otomatik set edilemez 

#------------------------------------------------------------
# 📒 Geliştirici Notu 2
#------------------------------------------------------------
# __context__, python'un kendisi için tuttuğu bir attribute'dur
# yani kullanıcının set etmesi beklenmez bu nedenle yukarıda anlatılanlar gerçekleşir
# ayrıca __cause__ eğer set edilmişse manuel veya from ile __context__ gösterilmez çünkü __suppress_context__ = True olmuştur.
#
# ------------------------------------------------------------
# 4️⃣ Örnek: Otomatik dolma
# ------------------------------------------------------------
try:
    int("abc")                # ValueError oluşur
except ValueError:
    1 / 0                     # ZeroDivisionError oluşur

# Bu örnekte ZeroDivisionError instance’ının __context__’i
# otomatik olarak ValueError instance’ına referans olur.
try:
    try:
        int("abc")
    except ValueError as e1:
        1 / 0
except ZeroDivisionError as e2:
    print("Şimdiki hata:", type(e2).__name__)
    print("Önceki hata (__context__):", repr(e2.__context__))

# Çıktı:
# Şimdiki hata: ZeroDivisionError
# Önceki hata (__context__): ValueError("invalid literal for int() with base 10: 'abc'")
#
# ------------------------------------------------------------
# 5️⃣ __context__ vs __cause__
# ------------------------------------------------------------
# - __context__ → raise from kullanılmazsa, önceki exception otomatik atanır.
# - __cause__   → raise from kullanılırsa manuel atanır, __context__ bastırılır.
#
# ------------------------------------------------------------
# 6️⃣ __suppress_context__ ile ilişkisi
# ------------------------------------------------------------
# - Bir exception’ın __suppress_context__ attribute’u True yapılırsa,
#   traceback’te __context__ bilgisi gösterilmez.
# - Bu genelde raise from kullanıldığında otomatik yapılır.
#
# ------------------------------------------------------------
# 7️⃣ Özet
# ------------------------------------------------------------
# __context__:
# - Bir exception, başka bir exception sırasında oluştuğunda otomatik dolar.
# - raise from kullanılmazsa devreye girer.
# - Hata zincirini görmek ve debug etmek için önemlidir.


def demo_A():
    try:
        raise KeyboardInterrupt("K1")
    except KeyboardInterrupt as ki:
        try:
            raise SystemExit("SE1")
        except SystemExit as se1:
            try:
                raise SystemExit("SE2")
            except SystemExit as se2:
                print("A: id(se2)       =", id(se2))
                print("A: id(se2.ctx)   =", id(se2.__context__))  # -> se1
                print("A: id(se1)       =", id(se1))
                print("A: id(se1.ctx)   =", id(se1.__context__))  # -> ki
                print("A: id(ki)        =", id(ki))

def demo_B():
    try:
        raise KeyboardInterrupt("K1")
    except KeyboardInterrupt as ki:
        try:
            raise SystemExit("SE1")
        except SystemExit as se1:
            try:
                raise se1  # aynı nesne
            except SystemExit as se2:
                print("B: id(se2)       =", id(se2))               # == id(se1)
                print("B: id(se2.ctx)   =", id(se2.__context__))   # -> ki
                print("B: id(se1)       =", id(se1))
                print("B: id(ki)        =", id(ki))

demo_A(); demo_B()

"""
KeyboardInterrupt("K1") oluşur.

except KeyboardInterrupt: içinde SystemExit("SE1") raise edilir → SE1.context = KI

except SystemExit as s: ile SE1 nesnesini yakaladın.

raise s dediğinde yeni bir SystemExit oluşturulmaz; aynı nesneyi tekrar fırlatırsın → s.__context__ değişmez, hâlâ KI.

👉 B’nin çıktısı KeyboardInterrupt("K1") olur.
"""

