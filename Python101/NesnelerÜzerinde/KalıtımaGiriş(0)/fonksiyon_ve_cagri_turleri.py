# Yüksek seviye çağrılar:
# obj.attr, getattr(obj, "attr"), setattr(obj, "attr", val), delattr(obj, "attr")

# → Python'un kullanıcıya sunduğu sade, okunabilir ve güvenli API'lardır
# → Hataları daha okunabilir hale getirir, hata durumlarında fallback mekanizmaları (örneğin __getattr__) devreye girer
# → Kodun taşınabilirliğini ve okunabilirliğini artırır
# → İçerikte descriptor olup olmadığını otomatik kontrol eder
# → Geliştiriciden detay gizler ama tam kontrol gerektiğinde düşük seviyeye geçişe izin verir
# → Python'un "easy to use, powerful if needed" felsefesini yansıtır

# Arkada çalışanlar:
# → getattr() → __getattribute__() + fallback olarak __getattr__()
# → setattr() → __setattr__()
# → delattr() → __delattr__()

# Bu fonksiyonlar aslında sadece kaplama (wrapper) gibidir, gerçek iş her zaman dunder metodlarca yapılır


# Düşük seviye çağrılar:
# obj.__getattribute__("attr"), obj.__setattr__("attr", val), obj.__delattr__("attr")

# → Bu metodlar doğrudan Python objelerinin iç davranışlarını tanımlar
# → Genellikle meta-programlama, debugger, descriptor yazımı veya sistem seviyesi araçlar tarafından kullanılır
# → Exception handling yapılmaz, doğrudan hatayı yükseltir
# → Sonsuz döngü (infinite recursion) riski taşır çünkü override edilmiş bir __getattribute__ içinde yine obj.attr dersen kendini çağırırsın
# → Dolayısıyla yalnızca bilinçli ve kontrollü kullanım içindir, genel kullanıcıya önerilmez
# → Gücün tamamını geliştiriciye verir ama koruma katmanlarını da kaldırır

# Kısacası:
# ✔ Yüksek seviye çağrılar → güvenli, kullanıcı dostu ve yaygın kullanım için
# ✔ Düşük seviye metodlar → doğrudan kontrol, güç ve özelleştirme için (ama tehlikeli olabilir)
