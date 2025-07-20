# ✅ PYTHON: __name__ ve __main__ Açıklaması

# 1️⃣ Her Python dosyası çalıştırıldığında, Python yorumlayıcısı o dosyaya özel bazı özel değişkenler oluşturur.
#    Bunlardan biri de: __name__

# 2️⃣ __name__ → Python tarafından otomatik olarak ayarlanır
#    Dosya:
#       - DOĞRUDAN çalıştırılıyorsa (örn. python dosya.py) → "__name__" değişkeni "__main__" olur
#       - İMPORT ediliyorsa → "__name__" değişkeni, dosya adı olur (örn. mymodule.py → __name__ = "mymodule")

# Bu değişken global scope’ta tanımlıdır (dosya düzeyinde)
#    → Yani bir fonksiyonun içinde tanımlı değildir, doğrudan çağrılabilir
# Python'da her çalışan dosya bir "main frame" başlatır
#    - Bu main frame: tüm global isimlerin (değişkenler, fonksiyonlar, sınıflar) saklandığı yerdir
#    - `__name__` de burada tutulur
# 3️⃣ "__main__" → Bu, özel bir tanımdır ve Python'da "Bu dosya çalıştırılıyor mu?" demektir


# 🧠 Yani:
#   - __name__ == "__main__" → bu kod dosyası direkt çalıştırılıyor
#   - __name__ == "modul_adi" → bu dosya bir başkası tarafından import edilmiş

# ✅ Bu bilgi, dosyanın nereden çalıştırıldığını anlamamızı sağlar

# 💡 Neden kullanılır?
#     Çünkü bazı kodlar sadece "ana program" olarak çalıştırıldığında çalışmalıdır.
#     Ama import edildiğinde çalışmamalıdır! (örneğin test, demo, vs.)

# 🔒 Bu yüzden bu yapıyı kullanırız:
if __name__ == "__main__":
    print("Bu dosya doğrudan çalıştırıldı!")  # ← bu satır sadece doğrudan çalıştırılınca yazdırılır
    # main() gibi bir fonksiyon başlatılabilir

if __name__ != "__main__":
    print(__name__)