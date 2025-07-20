# ==========================================================
# 🔁 OPERATÖR TASARIMI STRATEJİSİ (Pythonic ve Güvenli Yaklaşım)
# ==========================================================
#
# 🎯 Amaç:
#    ➤ Kendi sınıfının örnekleri arasında (+) işlemi normal şekilde çalışsın
#    ➤ Ancak özel türlerle (list, int vs.) birleşim gerektiğinde farklı davranış sergilensin
#
# ----------------------------------------------------------
# ✅ STRATEJİ:
# ----------------------------------------------------------
#
# 1️⃣ __add__:
#     - Sadece sınıfın kendi türüyle çalışır
#     - Örn: Alpha + Alpha gibi anlamlı işlemleri tanımlar
#     - Diğer türler için NotImplemented döner
#
# 2️⃣ __radd__:
#     - Eğer işlem senin sınıfınla başlamıyorsa (örn: list + Alpha),
#       ama bu özel durumları kontrol etmek istiyorsan burada tanımlanır
#     - list, str, int gibi diğer türler seni toplamak isterse burası devreye girer
#
# ----------------------------------------------------------
# 🔒 Neden bu yaklaşım güvenli?
# ----------------------------------------------------------
#
# - __add__ sade ve tahmin edilebilirdir
# - __radd__ ile sınıfını etkilemeden istisnaları yakalayabilirsin
# - Böylece toplama davranışı genişletilmiş olur ama bozma yapılmaz
#
# ----------------------------------------------------------
# 🧠 Özet:
# ----------------------------------------------------------
# ➤ Normal işlemler __add__ içinde tanımlanmalı
# ➤ Garip yazımlar veya özel türlerle işlem gerekiyorsa __radd__ içinde kontrol edilmeli
# ➤ Bu sayede esnek ama sağlam bir operatör davranışı sağlanır
#
# ==========================================================
