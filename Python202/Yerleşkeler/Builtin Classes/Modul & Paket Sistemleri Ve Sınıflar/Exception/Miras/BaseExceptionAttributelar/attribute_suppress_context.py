# ============================================================
# 📌 __suppress_context__ Attribute — Tanım ve Detaylar
# ============================================================

# ------------------------------------------------------------
# 1️⃣ Nedir?
# ------------------------------------------------------------
# - Bir exception instance’ının __suppress_context__ attribute’u,
#   traceback çıktısında __context__ bilgisinin gösterilip gösterilmeyeceğini
#   kontrol eden boolean bir bayraktır (True/False).
#
# - Varsayılan değeri: False
# - raise ... from ... kullandığında Python bunu otomatik True yapar.
#   otomatik set edilen bir attribute'değildir 
#
# ------------------------------------------------------------
# 2️⃣ Neden var?
# ------------------------------------------------------------
# - Normalde bir exception başka bir exception işlenirken oluşursa
#   (__context__ otomatik dolarsa), traceback çıktısında önceki hata da görünür.
#
# - Bazı durumlarda önceki hatayı göstermek istemeyebilirsin:
#   ✔ Kullanıcıya teknik detay sızmasını engellemek
#   ✔ Loglarda gereksiz bilgi kalabalığını önlemek
#   ✔ Sadece son hatayı ön plana çıkarmak
#
# ------------------------------------------------------------
# 3️⃣ raise ... from ... ile ilişkisi
# ------------------------------------------------------------
# - raise NewError(...) from old_error dediğinde:
#     NewError.__cause__ = old_error
#     NewError.__suppress_context__ = True
#   → Bu durumda traceback’te __context__ kısmı görünmez,
#     onun yerine __cause__ kısmı gösterilir.
#
# ------------------------------------------------------------
# 4️⃣ Manuel kullanım örneği
# ------------------------------------------------------------
try:
    int("abc")
except ValueError as e1:
    new_exc = RuntimeError("Yeni hata")
    new_exc.__context__ = e1            # Önceki hatayı manuel set ettik
    new_exc.__suppress_context__ = True # Önceki hata traceback'te gizlensin
    raise new_exc

# Bu örnekte:
# - Normalde ValueError traceback'te "During handling of the above exception..." kısmıyla görünürdü.
# - Ama __suppress_context__ = True olduğu için görünmez.
#
# ------------------------------------------------------------
# 5️⃣ Özet
# ------------------------------------------------------------
# __suppress_context__:
# - True ise, traceback’te __context__ bilgisi bastırılır.
# - False ise, __context__ traceback’te görünür.
# - raise ... from ... genelde bunu otomatik True yapar.
# - Hata zincirini kontrol etmek ve çıktı formatını sadeleştirmek için kullanılır.
