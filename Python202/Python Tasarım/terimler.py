# =============================================================================
#  PYTHON TERİM DÜZELTME TABLOSU — DOĞRU TEKNİK KULLANIM
# =============================================================================
# Bu tablo, Python öğreniminde sık yapılan terim hatalarını ve doğru karşılıklarını içerir.
# Format:
#   1) Doğru Terim (Ad)
#   2) Sık Yapılan Hatalı İsim
#   3) Açıklama / Neden Yanlış Olduğu & Doğru Kullanımı
# =============================================================================

# -----------------------------------------------------------------------------
# 1) Yorumlayıcı (Interpreter)  |  Hatalı: Derleyici
# -----------------------------------------------------------------------------
# Python, özellikle CPython uygulamasında, kaynak kodu önce bytecode'a derler (compile)
# ardından bu bytecode'u yorumlayıcı (interpreter) çalıştırır.
# Tam anlamıyla "derleyici" değildir, C/C++ gibi dillerdeki compiler mantığıyla karıştırılmamalı.
# Doğru kullanım: "Python yorumlayıcısı" veya "CPython yorumlayıcısı"

# -----------------------------------------------------------------------------
# 2) Anlamsal (Semantic)  |  Hatalı: Tanımsal
# -----------------------------------------------------------------------------
# Programlama bağlamında "semantic" = ifadenin anlamı ile ilgili.
# "Tanımsal" ise tanım yapmakla ilgili, teknik bağlamda yanlış.
# Örn: "anlamsal hata" = kod sözdizimsel olarak doğru ama beklenen anlamı karşılamıyor.

# -----------------------------------------------------------------------------
# 3) Kimlik Karşılaştırması (Identity Comparison)  |  Hatalı: Değer Karşılaştırması
# -----------------------------------------------------------------------------
# "is" operatörü kimlik karşılaştırması yapar (nesne bellekte aynı mı?).
# "==" operatörü değer karşılaştırması yapar (içerikler eşit mi?).
# None gibi tekil (singleton) nesnelerde "is" kullanmak güvenli ve doğrudur.

# -----------------------------------------------------------------------------
# 4) Tekil Nesne (Singleton)  |  Hatalı: Sabit Nesne
# -----------------------------------------------------------------------------
# Singleton: Bellekte yalnızca tek örneği bulunan nesne.
# Sabit (constant): Değeri değişmeyen.
# Bu ikisi aynı kavram değildir.
# Örn: None, Ellipsis, NotImplemented → singleton; sayılar ise immutable olabilir ama singleton değildir.

# -----------------------------------------------------------------------------
# 5) Yer Tutucu (Placeholder)  |  Hatalı: Boş Değer
# -----------------------------------------------------------------------------
# Placeholder: Kodun ileride doldurulacak kısmını işaretler (örn: ..., pass).
# Boş değer (None) ile aynı kavram değildir.

# -----------------------------------------------------------------------------
# 6) İstisna (Exception)  |  Hatalı: Hata (Error)
# -----------------------------------------------------------------------------
# Exception: Python'da yakalanabilir hata türü (try/except ile).
# "Error" genel bir terim, istisna olmayan hatalar da olabilir (örn: SyntaxError yorumlayıcı seviyesinde çalışır).

# -----------------------------------------------------------------------------
# 7) Sinyal Değeri (Sentinel)  |  Hatalı: Varsayılan Parametre
# -----------------------------------------------------------------------------
# Sentinel: Özel durumu işaret eden benzersiz nesne.
# Varsayılan parametre: Fonksiyon imzasındaki başlangıç değeri.
# Sentinel, "hiç verilmedi" ile "None verildi" ayrımı gibi durumlarda kullanılır.

# -----------------------------------------------------------------------------
# 8) Dunder Metot (Double Underscore Method)  |  Hatalı: Özel Fonksiyon
# -----------------------------------------------------------------------------
# Dunder metodlar (__add__, __repr__) Python'un özel protokollerini çalıştırır.
# "Özel fonksiyon" terimi çok genel, dunder metodlar dilin belirli davranışlarını tetikler.

# -----------------------------------------------------------------------------
# 9) Tip İpucu (Type Hint)  |  Hatalı: Tip Kontrolü
# -----------------------------------------------------------------------------
# Tip ipucu: Statik analiz için verilen bilgi (örn: typing modülü ile).
# Python runtime'da bunları zorunlu kılmaz.
# Tip kontrolü: mypy, pyright gibi araçlarla yapılır.

# -----------------------------------------------------------------------------
# 10) Operatör Protokolü (Operator Protocol)  |  Hatalı: Operatör Mantığı
# -----------------------------------------------------------------------------
# Operatör protokolü, Python'un __add__, __radd__, __lt__ gibi metotları çağırma sırasını ve
# fallback mekanizmasını tanımlar.
# "Operatör mantığı" çok genel kalır, protokol belirli bir teknik terimdir.
# -----------------------------------------------------------------------------
