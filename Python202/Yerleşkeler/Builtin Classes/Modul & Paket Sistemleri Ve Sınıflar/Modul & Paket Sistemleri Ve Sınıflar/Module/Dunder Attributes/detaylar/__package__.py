# -----------------------------------------------
# Python'da __package__ NEYİ temsil eder?
# -----------------------------------------------

# __package__, modülün mantıksal olarak ait olduğu "paket adını" tanımlar.
# Bu, RELATIVE IMPORT'lar için Python'un modülün "nerede" olduğunu anlamasını sağlar.

# -----------------------------------------------
# 🧭 Ama bu paket adı NEREDEN başlar?
# -----------------------------------------------

# CEVAP: sys.path listesinde bulunan klasörlerden itibaren.
# Yani Python "nereye kadar yukarı çıkıp import'a başlasın?" diye sys.path'e bakar.

# ÖRNEK YAPI:
#
# /Users/demir/Desktop/proje/
# ├── deneme222.py
# └── projeler/
#     └── p2/
#         ├── mod.py      ← BURADA __package__ tanımlıyoruz
#         └── app.py

# sys.path Python tarafından şu şekilde ayarlanır:
# sys.path = ["/Users/demir/Desktop/proje", ...]

# Yani, PYTHON BURAYI kök kabul eder: "/Users/demir/Desktop/proje"

# Dolayısıyla, "projeler" buradaki ilk PAKET gibi davranır

# -----------------------------------------------
# 🔍 mod.py dosyasındaysan:
# -----------------------------------------------

# modülün tam mantıksal adı: "projeler.p2.mod"
# bu durumda __package__ = "projeler.p2" olmalıdır

# çünkü:
# - ".mod" son modül dosyanın kendisi (bunu yazmıyoruz)
# - "projeler.p2" modülün ait olduğu paket

# -----------------------------------------------
# ❌ Peki sadece __package__ = "p2" yazarsak ne olur?
# -----------------------------------------------

# Python, p2 adında BİR ÜST DÜZEY PAKET arar (yani sys.path içinde "p2" klasörü arar)
# Ama p2 "projeler" klasörünün içinde olduğu için bulamaz → ImportError

# -----------------------------------------------
# ✅ Neden 'projeler.p2' doğrudur?
# -----------------------------------------------

# Çünkü Python, sys.path'deki kökten itibaren alt paketleri bu şekilde arar
# Ve 'projeler' klasörü fiziksel olarak __init__.py olmasa bile,
# biz __package__ ile mantıksal olarak bunu tarif edebiliriz

# -----------------------------------------------
# 🧠 ÖZET AKILDA KALSIN:
# -----------------------------------------------

# - __package__ = modülün "mantıksal yolu"
# - bu yol, sys.path içinden başlayarak oluşturulur
# - sys.path = proje kökü → 'projeler' = ilk görünen klasör
# - __package__ = 'projeler.p2' ⇒ RELATIVE IMPORT için şarttır
# - üstteki klasör (project_root) hiçbir zaman __package__ içinde YER ALMAZ

# -----------------------------------------------


# sys.path, Python yorumlayıcısı çalıştırıldığında oluşturulur.

# Eğer "python script.py" ile çalıştırırsan:
# → sys.path[0] = script.py’nin bulunduğu klasör olur.

# Eğer "python -m paket.altpaket.modul" ile çalıştırırsan:
# → sys.path[0] = içinde bulunduğun çalışma dizini (cwd) olur, paket yolu buradan çözülür.

# Eğer REPL (python) veya IDE’den başlatırsan:
# → sys.path[0] = boş string "" olur, yani current working directory (os.getcwd()) temsil edilir.

# Eğer sys.path’i elle değiştirirsen:
# → import arama sırası senin verdiğin yeni değerlere göre çalışır.
