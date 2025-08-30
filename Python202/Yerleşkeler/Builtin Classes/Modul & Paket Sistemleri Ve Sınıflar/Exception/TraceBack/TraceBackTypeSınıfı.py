# ============================================================
# 📌 TracebackType (traceback nesnesi tipi) — Detaylı Tanım
# ============================================================

# ------------------------------------------------------------
# 1️⃣ Tanım
# ------------------------------------------------------------
# - TracebackType, Python’da exception oluştuğunda yaratılan traceback nesnelerinin sınıfıdır.
# - TracebackType,types modülü aracılığı ile erişilebilir ama bu seni yanıltmasın
# - bu sınıf C dilinde Cpython ile yazılmıştır bu nedenle miras alınamaz
# - doğrudan örneklenmesi ile ilgili bir hata olmasada pratikte bu traceback,saçmalayabilir veya doğru çalışmayabilir
# - bu nedenle örneklenmeside tavsiye edilmez doğal olarak oluşması beklenir

# ------------------------------------------------------------
# 2️⃣ Nereden erişilir?
# ------------------------------------------------------------
# - import types → types.TracebackType ile tipi kontrol edebilirsin.
# - Her exception nesnesinin __traceback__ attribute’u bir TracebackType objesidir (veya None).
# - sys.exc_info()[2] → traceback objesine ulaşmanın başka bir yolu.

import types, sys

try:
    1 / 0
except Exception as e:
    tb = e.__traceback__
    print(isinstance(tb, types.TracebackType))  # True

# ------------------------------------------------------------
# 3️⃣ Temel attribute’lar
# ------------------------------------------------------------
# TracebackType objelerinin 4 ana attribute’u vardır:
#
# tb_frame   → traceback’in işaret ettiği stack frame nesnesi (types.FrameType)
# tb_lasti   → bytecode içindeki son çalıştırılan talimatın index’i (CPython’a özel)
# tb_lineno  → hatanın oluştuğu satır numarası (int)
# tb_next    → bir önceki çağrıya ait traceback (TracebackType veya None)
#
# Bu sayede traceback zincirini adım adım gezebilirsin.


#-----------------------------------------------------------
# 4️⃣ Tipik Traceback Görselleştirmesi
#-----------------------------------------------------------
# hata mesajında gördüğün: 'File "C:\U...", line 5, in <module>' ifade tb_frame attribute'u aracılığı ile oluşur
# tüm bunlar; f'  File "{tb.tb_frame.f_code.co_filename}", line {lineno}, in {frame.f_code.co_name}' dir
# yani aslına bakacak olursan traceback,tb_frame'in görselleştirilmesidir bu geliştirici ve kullanıcı için okunabilir bir çıktı sağlar.ama asıl hazine tb_frame'de yatar.

try:
    def a():
        b()
    def b():
        c()
    def c():
        1 / 0
    a()
except Exception as e:
    tb = e.__traceback__
    while tb is not None:
        print("Fonksiyon:", tb.tb_frame.f_code.co_name)
        print("Satır:", tb.tb_lineno)
        tb = tb.tb_next

# ------------------------------------------------------------
# 4️⃣ Dunder attribute / metod durumu
# ------------------------------------------------------------
# TracebackType özel bir C tabanlı tiptir, dolayısıyla kendi tanımlı dunder metodları çok azdır.
# Başlıca olanlar:
# - __reduce__ / __reduce_ex__ → Pickle desteği (ama genelde manuel serialize edilmez)
# - __dir__ → attribute listesini döner
# - __class__ → <class 'traceback'> (yani TracebackType)
#
# TracebackType kendi başına __repr__ veya __str__ override etmez.
# print(tb) yaptığında anlamlı bir çıktı almazsın; traceback.format_tb() kullanmalısın.

# ------------------------------------------------------------
# 5️⃣ Neden var? Avantajları
# ------------------------------------------------------------
# ✔ Exception call stack’ini programatik olarak gezebilme
# ✔ Hata loglama / filtreleme / maskeleme
# ✔ Testlerde belirli satırda hata oluştu mu kontrol etme
# ✔ Debug araçları (pdb, IDE debugger) için temel veri yapısı
#
# TracebackType olmasa, sadece exception mesajını bilirdik, stack bilgisi kaybolurdu.

# ------------------------------------------------------------
# 6️⃣ Sık yapılan hata
# ------------------------------------------------------------
# ❌ TracebackType objesini saklayıp çok sonra kullanmak:
#    Frame nesneleri büyük bellek tutabilir (locals/globals referansları içerir).
#    Bu yüzden genellikle string’e dönüştürülüp (format_tb) saklanır, ham nesne tutulmaz.


# ============================================================
# 📌 Python Traceback Zinciri Mantığı
# ============================================================

# ------------------------------------------------------------
# 1️⃣ Traceback zinciri nedir?
# ------------------------------------------------------------
# bir exception aktif olduğunda raise edilen exception nesnesi için __traceback__ set edilir
# __traceback__ stack trace bilgilerini tutan bir nesnedir.
# ama yalnızca hatanın kaynağını temsil eder ama zincirin tamamını tb_next ile içinde tutar

# tb_next, exception zincirinde hatanın oluştuğu yerden itibaren bir üst çağrının call stack'ine
# geçmek için kullanılan traceback zincirlerinin halkalarını bağlayan bir attribute'dur

# hata mesajında traceback çıktısında zincirin tüm halkaları sıralanmış bir şekilde karşımıza çıkar
# en alttan(kaynak -> __traceback__) başlayarak en üste(üst çağrı -> tb_next) sıralanır


# ------------------------------------------------------------
# 3️⃣ Frame nesneleri ve traceback ilişkisi
# ------------------------------------------------------------
# - Her TracebackType objesi, bir "FrameType" objesini (tb_frame) tutar.
# - FrameType:
#     • f_code   → çalışmakta olan kod objesi
#     • f_locals → o anda geçerli yerel değişkenler
#     • f_globals→ global değişkenler
#     • f_back   → bir önceki frame (ama traceback zincirini oluşturmak için f_back yerine tb_next kullanılır)
#
# Yani traceback zincirinde ilerlerken aslında frame’ler üzerinden dolaylı olarak stack’i geziyorsun.

# ------------------------------------------------------------
# 4️⃣ Traceback zincirini adım adım gezme örneği
# ------------------------------------------------------------
import sys

def level1():
    level2()

def level2():
    level3()

def level3():
    1 / 0  # Hata burada olacak

try:
    level1()
except Exception as e:
    tb = e.__traceback__  # Zincirin başı (en son hata oluşan frame)
    while tb is not None:
        frame = tb.tb_frame
        print("Fonksiyon adı:", frame.f_code.co_name)
        print("Dosya:", frame.f_code.co_filename)
        print("Satır:", tb.tb_lineno)
        print("---")
        tb = tb.tb_next  # Zincirde bir önceki frame'e git

# ------------------------------------------------------------
# 5️⃣ Closure yapısı var mı?
# ------------------------------------------------------------
# - Traceback zincirinin kendisinde closure gibi "free variable capture" mantığı yok.
# - Ama zincirdeki her tb_frame, o anda geçerli scope'un locals() ve globals()’ını referans olarak tutar.
# - Yani traceback üzerinden frame'e ulaştığında o fonksiyonun kapanış (closure) değişkenlerine ulaşabilirsin.
# - Bu yüzden traceback nesnesi "state" taşır diyebiliriz, çünkü stack’teki o anki bağlamı (context) korur.
# - Ancak bu state "immutable" değildir → locals() değişebilir (ama çoğu zaman debug dışında değiştirilmez).

# ------------------------------------------------------------
# 6️⃣ Avantajı ne?
# ------------------------------------------------------------
# ✔ Tüm hata zincirini, hangi sırayla fonksiyonların çağrıldığını görebilirsin.
# ✔ Her adımda hangi kod dosyası ve satırda olduğunu bulursun.
# ✔ Hatanın bağlamına (locals/globals) ulaşabilirsin → çok güçlü bir debug imkanı.
# ✔ traceback.walk_tb() gibi fonksiyonlarla programatik analiz yapılabilir.

# ------------------------------------------------------------
# 7️⃣ Önemli uyarı
# ------------------------------------------------------------
# ❗ Traceback nesnesi ve frame’ler, orijinal scope’u REFERANS ile tuttuğu için
#    büyük veri veya hassas bilgi barındırabilir → prod ortamda dikkatli sakla.
# ❗ Traceback zinciri çok derinse bellek kullanımı artar.
# ❗ Bu nedenle log’a yazarken genelde string formatına dönüştürülür, ham obje saklanmaz.

# ------------------------------------------------------------
# 8️⃣ Traceback Hata Mesajı Çıktısı Anlamı
# ------------------------------------------------------------

# REFERANS:
r"""
Traceback (most recent call last):
  File "C:\Users\demir\OneDrive\Desktop\MufredatKonulari_nesne_tabanli\MufredatKonulari_nesne_tabanli\PythonTemelleri\projeler\demir_importlib\t\t2.py", line 24, in <module>
    raise e from None
  File "C:\Users\demir\OneDrive\Desktop\MufredatKonulari_nesne_tabanli\MufredatKonulari_nesne_tabanli\PythonTemelleri\projeler\demir_importlib\t\t2.py", line 19, in <module>
    f3()
    ~~^^
  File "C:\Users\demir\OneDrive\Desktop\MufredatKonulari_nesne_tabanli\MufredatKonulari_nesne_tabanli\PythonTemelleri\projeler\demir_importlib\t\t2.py", line 15, in f3
    f2()
    ~~^^
  File "C:\Users\demir\OneDrive\Desktop\MufredatKonulari_nesne_tabanli\MufredatKonulari_nesne_tabanli\PythonTemelleri\projeler\demir_importlib\t\t2.py", line 11, in f2
    f1()
    ~~^^
  File "C:\Users\demir\OneDrive\Desktop\MufredatKonulari_nesne_tabanli\MufredatKonulari_nesne_tabanli\PythonTemelleri\projeler\demir_importlib\t\t2.py", line 8, in f1
    f()
    ~^^
  File "C:\Users\demir\OneDrive\Desktop\MufredatKonulari_nesne_tabanli\MufredatKonulari_nesne_tabanli\PythonTemelleri\projeler\demir_importlib\t\t2.py", line 5, in f
    raise ZeroDivisionError
ZeroDivisionError
"""

# Hata mesajında stack trace zincirin halkaların tamamı karşımıza çıkar bu mesajı adım adım inceleyim şimdi

# Traceback: bu sana hata çıktısının stack trace bölümünün başladığını söyler

# (most recent call last): python call stack'leri ters kronojik sırayla sıralar dolasıyla;
# in içteki yani en allta bulunan stack, hatanın kaynağıdır en baştaki stack ise en önceki çağrıdır

# bu ters krnojik sıralama, traceback modulunde bulunan metodlar içinde geçerlidir ilk eleman en önceki çağrıyı(en yukardaki) temsil eder
# son eleman ise kaynaktır
