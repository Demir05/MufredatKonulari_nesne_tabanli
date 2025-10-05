# ===============================================================
# 📘 PYTHON RUNTIME VE DİNAMİKLİK — SENIOR SEVİYE İNCELEME
# ===============================================================

# 🔹 Kod yazarken IDE’ye yazdığın şey, henüz çalıştırılmamış bir kaynak koddur.
#     ➤ Bu kod, yorumlayıcı tarafından çalıştırıldığında “runtime” başlar.

# ---------------------------------------------------------------
# ✅ 1. Runtime nedir?
# ---------------------------------------------------------------

# 🔍 Python’da runtime, yorumlayıcının kodu satır satır işlemesiyle başlar.
#     - Kod derlenmeden çalıştırılır → bu da dinamikliği doğurur.
# Python “derlenmeden çalışır” denirken kast edilen şey, statik derleme gibi önceden sabitlenmiş bir analiz yapılmamasıdır.
# Kodun anlamı, tipi ve davranışı runtime’da şekillenir. Bu da Python’a büyük esneklik kazandırır ama aynı zamanda dikkat gerektirir.
# ---------------------------------------------------------------
# ✅ 2. Python neden dinamik bir dildir?
# ---------------------------------------------------------------

# ➤ Dinamik dil demek:
#     - Tip kontrolü çalışma zamanında yapılır (runtime type checking)
#     - Değişkenler önceden tanımlanmak zorunda değildir
#     - Kodun yapısı runtime’da değiştirilebilir (örneğin: eval, setattr, dynamic import)

# 🔍 Örnek:
#     x = 5          → x bir int
#     x = "hello"    → x artık str → tip değişti → yorumlayıcı bunu runtime’da kabul eder

# ---------------------------------------------------------------
# ✅ 3. IDE’ye kod yazmak ne anlama gelir?
# ---------------------------------------------------------------

# ➤ IDE’ye yazdığın kod, henüz yorumlanmamış bir metindir.
#     - Syntax kontrolü yapılabilir (statik analiz)
#     - Ama tip kontrolü ve davranış analizi runtime’da olur

# 🔍 Bu yüzden IDE’de hata görünmeyen bir kod, runtime’da patlayabilir:
#     - Örneğin: `x.upper()` → x aslında int ise → AttributeError oluşur

# ---------------------------------------------------------------
# ✅ 4. Dinamikliğin avantajları ve dezavantajları
# ---------------------------------------------------------------

# 🔸 Avantajlar:
#     - Geliştirme hızı yüksektir
#     - Refactoring kolaydır
#     - Meta-programlama mümkündür (örneğin: decorator, dynamic dispatch)

# 🔸 Dezavantajlar:
#     - Hatalar runtime’da ortaya çıkar → test şarttır
#     - Performans maliyeti olabilir (statik dillere göre daha yavaş)
#     - IDE desteği sınırlı olabilir (tip tahmini zor)

# ---------------------------------------------------------------
# ✅ 5. Runtime’da neler değişebilir?
# ---------------------------------------------------------------

# ➤ Python’da runtime’da:
#     - Yeni fonksiyon tanımlanabilir
#     - Modül yüklenebilir
#     - Sınıfın attribute’ları değiştirilebilir
#     - Kod çalışırken eval() ile yeni kod üretilebilir

# 🔍 Bu esneklik, Python’u güçlü ama dikkat gerektiren bir dil yapar.

# ---------------------------------------------------------------
# ✅ 6. Senior perspektifiyle yorum
# ---------------------------------------------------------------

# ➤ “Python dinamik bir dildir” demek, sadece tip sistemini değil,
#     runtime’daki davranış esnekliğini de kapsar.

# ➤ Bu, yazılım mimarisi kurarken:
#     - Tip güvenliği için test ve type hinting (mypy, pydantic) kullanmayı gerektirir
#     - Runtime’da oluşabilecek hataları öngörmek için exception handling şarttır
#     - Performans kritik yerlerde C extension veya PyPy gibi çözümler düşünülmelidir

# ---------------------------------------------------------------
# ✅ SONUÇ:
# ---------------------------------------------------------------

# ➤ IDE’ye yazdığın kod, yorumlayıcıya gönderilene kadar sadece metindir.
# ➤ Python yorumlayıcısı kodu runtime’da işler → bu da dinamikliği doğurur.
# ➤ Dinamiklik, esneklik sağlar ama kontrolü zorlaştırır → senior seviyede bu riskler yönetilmelidir.
