###############################################################
# 1. AŞAMA — KAYNAK EDİNİMİ ve ÖN İŞLEMLER
###############################################################


Bu aşama, Python yorumlayıcısının kaynak kodu okumaya başladığı
ilk andır. Hedefi; diskteki ham baytları alıp, lexer'ın (tokenizer'ın)
işleyebileceği temiz ve standart bir metin haline getirmektir.

Yani burada henüz “token”, “AST”, “bytecode” gibi yapılar yoktur.
Yalnızca diskte duran bir .py dosyası vardır — Python onu anlamlı
karakter dizilerine çevirmekle meşguldür.



# -------------------------------------------------------------
# 1.1 — Dosyanın Okunması (Bayt Düzeyinde)
# -------------------------------------------------------------
"""
Yorumlayıcı ilk olarak, kaynak dosyayı diskteki halinden okur.
Bu okuma işlemi bayt (byte) düzeyindedir, çünkü dosya sisteminde
her şey ikili (binary) formda saklanır.

Eğer bir dosya çalıştırılıyorsa:
    PyParser_ASTFromFileObject()  (C düzeyinde)
Eğer REPL ortamındaysa:
    PyRun_InteractiveOneObject()

Fonksiyonları devreye girer.
"""

örnek_dosya = open("main.py", "rb")  # binary modda okuma
veri = örnek_dosya.read()
print(veri[:20])  # b'# -*- coding: utf-8 -*-'

"""
Bu aşamada Python henüz karakterleri tanımıyordur,
sadece bayt dizisi elindedir.
"""


# -------------------------------------------------------------
# 1.2 — Kodlama (Encoding) Tespiti — PEP 263
# -------------------------------------------------------------
"""
Python, kaynak kodların hangi karakter setiyle (UTF-8, Latin-1 vb.)
yazıldığını bilmek zorundadır. Bunu anlamak için dosyanın
ilk iki satırını geçici olarak ASCII kabul eder.

ASCII karakterler tüm encodinglerde aynı olduğu için bu güvenlidir.
Eğer şu tür bir satır görürse:
    # -*- coding: utf-8 -*-
veya
    # coding: latin-1
bunu “resmî encoding” olarak kabul eder.
Eğer böyle bir satır yoksa, varsayılan olarak UTF-8 seçilir.

Bu davranış, PEP 263 adlı standarda dayanır.
"""
örnek_kodlama_satırı = b"# -*- coding: utf-8 -*-\nprint('merhaba')"
# Python bu baytları ASCII alt kümesinde okuyabilir,
# çünkü '#' , '-' , 'c', 'o', 'd', 'i', 'n', 'g' karakterleri
# tüm encodinglerde aynı konumda bulunur.


# -------------------------------------------------------------
# 1.3 — BOM (Byte Order Mark) Kontrolü
# -------------------------------------------------------------
"""
Bazı UTF-8 veya UTF-16 dosyalarının başında görünmez bir işaret bulunur:
    EF BB BF
Bu baytlar dosyanın "Unicode" olduğunu belirtir, ancak kodun
içinde görünmemesi gerekir. Python bu işareti fark eder ve temizler.

Aksi halde dosya şu şekilde başlardı:
    '\ufeffprint("selam")'
ve lexer ilk karakteri '\ufeff' olarak algılardı.
Bu da SyntaxError’a yol açardı.
"""


# -------------------------------------------------------------
# 1.4 — Baytların Unicode Karakterlerine Dönüştürülmesi
# -------------------------------------------------------------
"""
Encoding belirlendikten sonra, Python artık baytları decode eder.
Yani, 0x78 0x20 0x3d 0x20 0x35 0x0a  →  "x = 5\n"

Artık diskteki ham baytlar yerine, bellekte gerçek Unicode
karakterler vardır. Python’un dil kuralları hep Unicode
karakterler üzerinden çalışır.
"""

örnek_baytlar = b"x = 5\n"
örnek_karakterler = örnek_baytlar.decode("utf-8")
print(örnek_karakterler)  # x = 5


# -------------------------------------------------------------
# 1.5 — Satır Sonlarını Normalize Etme
# -------------------------------------------------------------
"""
Farklı işletim sistemleri farklı satır sonları kullanır:
    Windows: \r\n
    Unix/Linux/macOS: \n
    Eski Mac: \r

Lexer, satır sonlarını tek bir biçimde görmek ister. Bu yüzden
Python tüm varyasyonları '\n' haline getirir.

Böylece token’lar oluşturulurken satır sınırları hep tutarlı olur.
"""

örnek = "print(1)\r\nprint(2)\r\n"
normalize = örnek.replace("\r\n", "\n")
print(normalize.splitlines())  # ['print(1)', 'print(2)']


# -------------------------------------------------------------
# 1.6 — Satır Bazlı Akış (Stream) Hazırlama
# -------------------------------------------------------------
"""
Lexer tüm dosyayı bir defada değil, satır satır işler.
Bu yüzden Python, kaynak kodu “okuma akışı” (readline) biçiminde sunar.

Bu akış nesnesi:
    - Bir dosyanın .readline() fonksiyonu olabilir
    - Ya da bir string için io.StringIO nesnesi olabilir

Bu yapı sayesinde lexer, her satırı sırasıyla okuyup
token üretir.
"""

import io
örnek_kod = "x = 5\nprint(x)\n"
akış = io.StringIO(örnek_kod)
print(akış.readline())  # x = 5
print(akış.readline())  # print(x)


# -------------------------------------------------------------
# 1.7 — Sonuç: Lexer’a Hazır Temiz Kaynak Metin
# -------------------------------------------------------------
"""
Tüm bu işlemlerden sonra Python’un elinde artık:
    ✅ Unicode karakterlerden oluşan bir kaynak
    ✅ BOM’dan arındırılmış
    ✅ Satır sonları normalize edilmiş
    ✅ Kodlaması belirlenmiş
    ✅ Satır bazlı okunabilir bir akış
bulunur.

Artık lexer (tokenizer) devreye girip bu metni karakter
karakter tarayabilir.
"""

"""
Kısacası: 
Kaynak edinimi ve ön işlemler aşaması, Python’un diskteki
ham dosyayı “yorumlanabilir metin” haline getirdiği aşamadır.
Lexer bu hazırlık sayesinde hatasız çalışır.
"""
