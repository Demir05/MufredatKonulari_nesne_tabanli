# ===============================================================
# 🎭 TİYATRO METAFORU — "Coroutine" vs "Nested Class"
# ===============================================================
# 🔸 Coroutine: Bir oyuncu tüm replikleri sırayla söyler.
#     - Fonksiyon ilerler, await der, durur, devam eder
#     - Sahne yönetimi tek oyuncuda: akış lineer
#
# 🔸 Nested Class: Her oyuncu kendi sahnesinde oynar
#     - Her state (Idle, Running, Done) ayrı sınıf
#     - Sahne bitince başka bir oyuncuya (sınıfa) geçilir
#     - OOP + modülerlik = yapılandırılmış kontrol
#
# ===============================================================
# 🧠 ZİHİNSEL MODEL
# ===============================================================
# Coroutine = Fonksiyon tabanlı, zamana/akışa odaklı
#             "Kod sırayla akar, bekleyebilir"
#
# Nested Class = Sınıf tabanlı, duruma/organizasyona odaklı
#                "Her durum ayrı bir sınıf, kod modular"

# ===============================================================
# 🛠 KULLANIM STRATEJİSİ
# ===============================================================
# 🧵 Coroutine:
# - Async IO işlemler (sleep, fetch, socket)
# - Zaman uyumlu modeller (trafik ışığı zamanlı)
# - Küçük, tek akışlı sistemler

# 🏗 Nested Class:
# - Büyük state graph’lar
# - OOP temelli davranışlı geçişler
# - IDE + test kolaylığı isteyen sistemler

# BONUS:
# 🧬 Hibrit model: Nested class + coroutine = power duo
# ===============================================================
