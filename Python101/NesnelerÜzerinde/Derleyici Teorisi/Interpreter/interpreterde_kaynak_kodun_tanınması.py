# ===============================================================
# 📘 CPython’DA ATTRIBUTE TANIMA & PERFORMANS OPTİMİZASYONLARI
# ===============================================================
# Bu rehber, CPython’un bazı özel metot ve attribute’ları nasıl “tanıdığı”nı,
# bu tanımanın yorumlama sürecine etkisini ve performans açısından ne farklar ortaya çıkabileceğini açıklar.

# ---------------------------------------------------------------
# ✅ 1. CPython’un “doğrudan tanıdığı” attribute/metotlar
# ---------------------------------------------------------------
# Tüm python yerleşkeleri Cpython'un kaynak kodlarında tanımlı olup kendilerine özel opcode'lara sahiptirler.
# bu nesnelere,interpreter'in tanıdığı/tanımlı olduğu nesneler denebilir.
# yalnız bu "tanıma" doğrudan nesnenin sahip olduğu(str,int,float,def) gibi isimler değil runtime ile beraber;
# kodun derlenmesiyle oluşan bytecode içindeki opcode'lardır çünkü yürütme motoru sadece bu opcode'lardan emir alır
# ayrıca bu özel opcode'lar, genel opcode'lara göre doğrudan C düzeyinde işlem yaparlar bu durumda daha az opcode oluşur;
# daha az opcode oluşması demek yürütme motorunun daha az çalışması ki bu performansı ciddi oranda etkiler
# işte bu durumda özel opcode ile ilişkilendirilimiş olan nesneye "tanınan" nesne denir

# 🧩 Örnek:
#     Python yerleşesi olan bir sınıfta (int olsun) 10 + 10 yapıldığında attribute çözümlemesi ile __add__ metodu değil, derleme sonrasında ilgili olan opcode;
#     yürütme motoru tarafından doğrudan C düzeyinde işlem yapar bu durumda daha az overhead'e takılırır bu da performansı ciddi oranda attrırır
#     ama user definded class'larda bunlar olmaz bu nedenle normal attribute erişim mekanizması devrededir bu özel değil genel opcode kullanmak demek, genel opcode kullanmak;
#     yürütülmesi gereken daha fazla opcode anlamına gelir tüm bunlar performansı zayıflatır.

# 🔍 RealPython’da, CPython’un “internals” derslerinde bu “özellik tanıma + optimize etme” stratejileri vurgulanır. :contentReference[oaicite:0]{index=0}

# ---------------------------------------------------------------
# ✅ 2. Bu tanıma sürecinin nasıl işlediği?
# ---------------------------------------------------------------
# 🔸 CPython,kaynak kodu önce token'lara ayırır.
# 🔸 CPython kodu sonrasında bir AST’ye (soyut sözdizim ağacı) çevrilir.
# 🔸 Sonra derleyici (compiler), AST’yi CodeType’a çevirir.
# 🔸 Bytecode içinde, bazı işlemciler (builtin işlemler) için özel opcode’lar yer alır.
# 🔸 Yürütme Motoru (eval loop), bu opcode’ları C düzeyinde tanır ve doğrudan çalıştırır.

# 📌 Örneğin:
#     result = len(my_list)
#     → Bytecode: LOAD_GLOBAL len → CALL_FUNCTION

# ---------------------------------------------------------------
# ✅ 3. Tanınmayan davranışlar nasıl yürütülür?
# ---------------------------------------------------------------
# 🔸 Kullanıcının tanımladığı metotlar veya sınıflar → CPython tarafından “bilinmeyen” olarak kabul edilir.
# 🔸 Bunlar bytecode’a çevrilir ve eval loop içinde adım adım yorumlanır.
# 🔸 Bu yorumlama, her opcode için yığın işlemleri, tip kontrolleri, hata kontrolleri içerir.

# 🧮 Örnek:

# def my_sum(lst):
#     total = 0
#     for x in lst:
#         total += x
#     return total

# → Bu fonksiyonun kodu, çeşitli LOAD / STORE / BINARY_ADD opcode’larına ayrılır
# → Her iteration’da bu opcode’lar yorumlayıcı tarafından işlenir — => daha fazla yük

# ---------------------------------------------------------------
# ✅ 4. Performans farkı nasıl ortaya çıkar?
# ---------------------------------------------------------------
# 🔸 Tanınan işlemler:
#     • C ile uygulanmış kod yolları (fast path)
#     • Daha az kontrol (tip kontrolü, hata kontrolü) gerekir
#     • Daha az bellek hareketi → daha yüksek hız

# 🔸 Tanınmayan işlemler:
#     • Çok sayıda opcode içerir
#     • Yorumlayıcı döngüsünde çok daha fazla işlem geçer
#     • Tip kontrolü, hata yakalama, stack yönetimi gibi “ek yükler” vardır

# ⚡ Bu fark özellikle *sık kullanılan*, *döngü içinde çalışan* veya *kritik performans noktası* kodlarda göze çarpar.

# ---------------------------------------------------------------
# ✅ 5. Gerçekçi Karşılaştırma (senin kod ↔ builtin)
# ---------------------------------------------------------------
# ➤ sum([1, 2, 3])  → yerleşik C kodu, optimize edilmiş yol
# ➤ kullancı my_sum(some_list) → Python kodu, daha fazla opcode + yorumlayıcı yükü

# ➤ Aynı işi yapsalar da, sum çok daha hızlı olur — özellikle büyük listelerde bu fark büyür.

# ---------------------------------------------------------------
# ✅ 6. Bu “attribute tanıma” CPython’a ne kazandırır?
# ---------------------------------------------------------------
# ➤ Özel metotlar için:
#     • Daha kısa opcode dizileri
#     • C koduna geçiş (fast path)
#     • Düşük seviye optimizasyonlardan faydalanma (örneğin vectorcall, inline optimizasyonlar)

# ➤ Genel (tüm sınıf/metotlar için geçerli olmayan) yollar daha ağırdır, çünkü yorumlayıcı tüm durumu kontrol etmek zorundadır.

# 📆 Örneğin, CPython 3.13 ve sonraki sürümlerde, “super instruction” tekniği ile art arda gelen opcode’lar birleştirilerek yorumlama maliyeti azaltılıyor. (örneğin LOAD_FAST + LOAD_FAST birleşik opcode’da işleniyor) :contentReference[oaicite:1]{index=1}
# Ayrıca bazı built-in fonksiyon çağrılarında vectorcall kullanımı performans kazancı sağlıyor. :contentReference[oaicite:2]{index=2}


# 🚀 VECTORCALL OPTİMİZASYONU DERLEMESİ
# Amaç: Fonksiyon çağrılarında tuple/dict tahsisi olmadan doğrudan C dizisi ile argüman iletmek
# Kaynak: PEP 590, CPython 3.9+ sürümleri

# ✅ 1. Vectorcall aktif olma koşulları
# - Sınıfın Py_TPFLAGS_HAVE_VECTORCALL bayrağı aktif olmalı
# - tp_call slot'u PyVectorcall_Call ile eşlenmiş olmalı
# - tp_vectorcall_offset doğru tanımlanmalı
# - __call__ metodu override edilmemiş olmalı

# ❌ 2. __call__ override edilirse ne olur?
# - CPython, __call__ yeniden tanımlandığında vectorcall bayrağını otomatik kaldırır
# - Sonradan object.__call__ ile geri dönülse bile bayrak geri gelmez
# - Yani vectorcall devre dışı kalır → PyObject_Call() kullanılır

# ⚠️ 3. *args ve **kwargs kullanımı
# - Fonksiyon *args veya **kwargs ile tanımlanmışsa:
#   → Python yorumlayıcısı zaten tuple/dict oluşturmak zorundadır
#   → Bu durumda vectorcall avantajı kaybolur
# - Vectorcall, sabit argümanlı fonksiyonlarda daha etkilidir

# 🧠 4. Ne zaman vectorcall tercih edilmeli?
# - Fonksiyon sabit sayıda argüman alıyorsa (örneğin def f(a, b, c): ...)
# - Sınıf __call__ override etmiyorsa
# - Fonksiyon sık ve performans kritik çağrılıyorsa

# 🧩 5. Stratejik öneri
# - __call__ yerine ayrı bir run() metodu tanımlanabilir → vectorcall korunur
# - Dinamik çağrılar için esneklik gerekiyorsa vectorcall’dan bilinçli olarak vazgeçilir

# 🔍 6. Manuel kontrol (C API düzeyinde)
# - PyVectorcall_Function(obj) != NULL → vectorcall destekleniyor
# - Python’dan doğrudan erişim yok, sadece C düzeyinde introspection(kendini inceleme) mümkün

# 📌 7. Belgelenmiş davranış (Python 3.12+)
# - __call__ yeniden atanırsa → vectorcall bayrağı kaldırılır
# - Bu davranış CPython’un güvenlik ve semantik uyum politikası gereğidir

# 🧠 Sonuç:
# Vectorcall, yüksek performans için güçlü bir araçtır ama semantik esneklikle çelişebilir.
# Kodun mimari evriminde bu optimizasyonu korumak için sınıf tasarımı ve çağrı protokolü dikkatle yapılandırılmalıdır.

# ---------------------------------------------------------------
# ✅ 7. Uyarılar & Sınırlamalar 🛡️
# ---------------------------------------------------------------
# ⚠️ Her şey bu şekilde optimize edilemez — esneklik, dinamiklik kaybolur.
# ⚠️ Yorumlayıcının bu tanıma stratejisi bazen “special-casing” mirasını taşır — karışıklık yaratabilir.
# ⚠️ Yeni Python sürümleriyle bazı optimizasyonlar değişebilir, bu yüzden kodun “performans hack’i” çok bağımlı hale gelmemeli.

# 🧩 Yani: optimize edilen yollar güçlüdür, ama her yeri bu yollara uydurmak kod karmaşıklığı getirir.

# ---------------------------------------------------------------
# ✅ SONUÇ
# ---------------------------------------------------------------
# ➤ CPython, bazı özel metot ve attribute’ları doğrudan tanıyarak onları “fast path” olarak işler.
# ➤ Bu tanıma süreci, bytecode + opcode + yorumlayıcı optimizasyonuyla birleştirilir.
# ➤ Böylece, yerleşik işlemler ile kullanıcı işlemleri arasında büyük hız farkları ortaya çıkar.
# ➤ Kod yazarken bu farkları bilmek, performans kritik yerlerde doğru seçimler yapmanı sağlar — senin gibi ileri düzey geliştiriciler için bu ayrım fark yaratır.
