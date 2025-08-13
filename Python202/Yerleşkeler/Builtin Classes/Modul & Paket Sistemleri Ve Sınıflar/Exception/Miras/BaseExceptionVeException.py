# ============================================================
# 📌 PYTHON'DA EXCEPTION SINIFLARI — NESNE MODELİ
# ============================================================

# =========================
# 1️⃣ BaseException
# =========================
# - Python’daki TÜM exception’ların kök sınıfıdır.
# - Doğrudan object’ten türetilmiştir (object → BaseException).
# - Exception, SystemExit, KeyboardInterrupt gibi tüm tipler bundan miras alır.
#
# class BaseException(object):
#     __module__ = 'builtins'
#
#     def __init__(self, *args: object) -> None:
#         # Exception'a verilen parametreler tuple olarak args içinde tutulur.
#         self.args = args


#object
#     └── BaseException
#           ├── Exception
#           │     ├── ArithmeticError
#           │     │     ├── ZeroDivisionError
#           │     │     └── OverflowError
#           │     ├── LookupError
#           │     │     ├── IndexError
#           │     │     └── KeyError
#           │     ├── ValueError
#           │     ├── TypeError
#           │     ├── OSError
#           │     └── ... (daha birçok yerleşik hata tipi)
#           ├── SystemExit
#           ├── KeyboardInterrupt
#           └── GeneratorExit
#
# 💡 ÖNEMLİ:
# - BaseException doğrudan “object”ten türetilmiştir.
# - Exception ise BaseException’ın alt sınıfıdır ve genelde
#   kullanıcı tanımlı exception’lar bundan türetilir.
# - SystemExit, KeyboardInterrupt, GeneratorExit → Exception’dan değil,
#   doğrudan BaseException’dan türetilmiştir (bilerek; bunlar özel sinyallerdir).
#   Kullanıcı genelde except Exception:... dediği için ve bu sinyallerde
#   programın düzgün sonlanabilmesi için kritik olduğundan, yakalanmamaları için böyle bir kaltıtım uygulanmıştır
#   Not: except:... çıplak bir şekilde kullanıldığında bu sinyaller'de yakalanır.

# ------------------------------------------------------------
# 📌 Bu sınıfa ÖZEL dunder attribute'lar:
# ------------------------------------------------------------
# Bunlar Python’da sadece BaseException ve alt sınıflarında bulunur.
#
# 1) __cause__  → Exception Chaining (Zincirleme)
#    - raise from kullanıldığında set edilir:
#         raise YeniHata() from OrijinalHata()
#    - Manuel olarak da atanabilir: e.__cause__ = başka_exception
#    - Amacı: Traceback'te "The above exception was the direct cause of..." bölümünü göstermek.
#
# 2) __context__ → Otomatik Exception Bağlamı
#    - raise from kullanılmazsa, ve bir exception işlenirken başka bir exception oluşursa,
#      Python otomatik olarak önceki exception’ı __context__ içine koyar.
#    - Bu da traceback’te "During handling of the above exception, another exception occurred" şeklinde görünür.
#
# 3) __suppress_context__ → Bağlam Bastırma
#    - True yapılırsa __context__ traceback’te gösterilmez.
#    - Özellikle raise from ile __cause__ kullandığında otomatik olarak True olur.
#    - Gerektiğinde manuel olarak da set edilebilir.
#
# 4) __traceback__ → Traceback Nesnesi
#    - Exception oluştuğunda, ilgili call stack’in bilgilerini tutar.
#    - traceback modülü ile detaylı olarak gezilebilir.
#    - __traceback__.tb_frame → o anki frame objesi
#    - __traceback__.tb_lineno → satır numarası
#    - __traceback__.tb_next → zincirdeki bir sonraki traceback
#
# ------------------------------------------------------------
# 📌 BaseException Metodları:
# ------------------------------------------------------------
# - __str__(self)  → Tek argüman varsa onu stringe çevirir, birden fazla varsa tuple olarak döner.
# - __repr__(self) → Sınıf adını ve args değerini döner (debug görünümü).
# - __reduce__(self) → Pickle için nasıl serileştirileceğini belirtir.
# - with_traceback(tb) → Exception nesnesine traceback objesi ekler (return self).
#
# Örnek:
try:
    1 / 0
except ZeroDivisionError as e:
    print("args:", e.args)
    print("__cause__:", e.__cause__)
    print("__context__:", e.__context__)
    print("__traceback__:", e.__traceback__)

# ============================================================
# 2️⃣ Exception
# ============================================================
# - BaseException’ın alt sınıfı.
# - Günlük hayatta yazdığımız/tanımladığımız exception’ların çoğu bundan türetilir.
# - Kendi özel dunder attribute’u yoktur; tüm altyapı BaseException’dan gelir.
#
# class Exception(BaseException):
#     pass
#
# 💡 Not:
#   - Exception’ın asıl amacı “normal hata” tiplerini toplamak.
#   - SystemExit, KeyboardInterrupt, GeneratorExit → Exception’dan değil,
#     doğrudan BaseException’dan türetilmiştir ki “except Exception” ile yakalanmasınlar.
#
# ============================================================
# 📌 ÖZET
# ============================================================
# - BaseException: args + (__cause__, __context__, __suppress_context__, __traceback__) attribute’larını taşır.
# - Exception: BaseException’ın normal hata tipleri için alt sınıfı.
# - __cause__: raise from ile doğrudan sebep zinciri
# - __context__: otomatik bağlam (başka exception işlenirken oluşan)
# - __suppress_context__: True ise __context__ traceback’te gizlenir
# - __traceback__: hatanın oluştuğu yerin tüm stack bilgisi
