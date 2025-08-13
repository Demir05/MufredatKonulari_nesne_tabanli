# ============================================================
# 📌 __traceback__ Attribute — Tanım ve Detaylar
# ============================================================

# ------------------------------------------------------------
# 1️⃣ Nedir?
# ------------------------------------------------------------
# - Bir exception instance’ının __traceback__ attribute’u,
#   o exception oluştuğunda Python yorumlayıcısının yakaladığı
#   "stack trace" bilgisini tutan özel bir nesnedir.
#
# - Türü: types.TracebackType
# - Bu nesne zincir şeklinde (linked list) önceki çağrı stack’lerini tutar.
#
# ------------------------------------------------------------
# 2️⃣ İçinde ne var?
# ------------------------------------------------------------
# TracebackType nesnesinin önemli alanları:
#   tb_frame   → Hatanın oluştuğu "frame" (FrameType)
#   tb_lineno  → O frame içindeki hata satır numarası
#   tb_next    → Bir önceki frame’in traceback’i (zincir)
#
# FrameType içindeki:
#   f_code     → CodeType nesnesi (fonksiyon/dosya bilgileri)
#       co_filename → Kaynak dosya yolu
#       co_name     → Fonksiyon adı
#       co_firstlineno → Fonksiyonun başladığı satır
#   f_locals   → O anki local değişkenler dict’i
#   f_globals  → Global değişkenler dict’i
#
# ------------------------------------------------------------
# 3️⃣ Nasıl oluşur?
# ------------------------------------------------------------
# - Bir exception raise edildiğinde Python yorumlayıcısı,
#   o anda yürütülmekte olan call stack’in bilgilerini alır
#   ve __traceback__ içine yerleştirir.
# - Exception zinciri (__context__, __cause__) takip edilerek
#   her bir exception kendi traceback’ini taşır.
#
# ------------------------------------------------------------
# 4️⃣ Kullanım alanları
# ------------------------------------------------------------
# ✔ Loglama → Hatanın nerede, hangi dosyada, hangi satırda çıktığını bulmak.
# ✔ Debug → O anki local/global değişkenleri incelemek.
# ✔ Özel hata raporlama → Kendi traceback formatını oluşturmak.
#
# ------------------------------------------------------------
# 5️⃣ Örnek kullanım
# ------------------------------------------------------------
import types

try:
    int("abc")
except ValueError as e:
    tb = e.__traceback__  # TracebackType instance
    print(isinstance(tb, types.TracebackType))  # True

    # Hata satırını ve dosyasını bulma
    print("Dosya:", tb.tb_frame.f_code.co_filename)
    print("Fonksiyon:", tb.tb_frame.f_code.co_name)
    print("Satır:", tb.tb_lineno)

    # O anki local değişkenler
    print("Local değişkenler:", tb.tb_frame.f_locals)

# ------------------------------------------------------------
# 6️⃣ Özet
# ------------------------------------------------------------
# __traceback__:
# - Exception’ın oluştuğu andaki tüm stack bilgisini saklar.
# - TracebackType zinciri üzerinden geçmiş çağrıları takip edebilirsin.
# - Doğrudan manipüle edilebilir (örn. exc.__traceback__ = None → traceback gizlenir)
# - Exception raporlama, loglama ve debugging için çok önemlidir.

