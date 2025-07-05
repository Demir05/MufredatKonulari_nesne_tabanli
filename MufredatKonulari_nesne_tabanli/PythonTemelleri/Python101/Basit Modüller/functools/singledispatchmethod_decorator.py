# 🧠 @singledispatchmethod NEDİR?

# `@singledispatchmethod`, `@singledispatch` ile aynı mekanizma üzerine kuruludur.
# FAKAT: sınıf yöntemleri (instance methods) için özel olarak tasarlanmıştır.
# Çünkü `@singledispatch` yalnızca modül düzeyi (bağımsız) fonksiyonlarla çalışabilir.

# `@singledispatchmethod`, ilk argümanın `self` olduğu metotlar için tip tabanlı dispatch desteği sağlar.
# Yani hangi tipte veri gönderildiğine göre farklı methodların çalışmasını mümkün kılar.

# Bu özellik Python 3.8+ sürümleriyle `functools` modülüne eklenmiştir.


# 🧩 TEMEL FARKI NEDİR?
# - `@singledispatch`: sadece global fonksiyonlar için uygundur
# - `@singledispatchmethod`: sınıf metotları için kullanılır (ilk parametre 'self' olmalıdır)

# 📚 Ortak Noktaları:
# - Her ikisi de `register()` ile yeni tip-fonksiyon eşlemesi ekler
# - `dispatch()` ile elle uygun fonksiyonu alabiliriz
# - `registry` özelliği vardır (kayıtlı tip-fonksiyon tablosu)

# 🔧 TEMSİLİ BİR SINIF (simplified)
class SingleDispatchMethod:
    def __init__(self, func):
        self.default_func = func
        self.registry = {}

    def register(self, typ):
        def wrapper(func):
            self.registry[typ] = func
            return func
        return wrapper

    def dispatch(self, typ):
        return self.registry.get(typ, self.default_func)

    def __get__(self, instance, owner):
        # 💡 Descriptor davranışı
        def method(arg, *args, **kwargs):
            fn = self.dispatch(type(arg))
            return fn(instance, arg, *args, **kwargs)  # self → instance
        return method


# 🎨 KULLANIM ÖRNEĞİ
class Printer:
    @SingleDispatchMethod
    def display(self, arg):
        return f"Generic: {arg}"

    @display.register(str)
    def _(self, arg):
        return f"Metin: {arg}"

    @display.register(int)
    def _(self, arg):
        return f"Sayı: {arg}"
        
# 🎬 Deneme
p = Printer()
print(p.display("merhaba"))  # ➜ Metin: merhaba
print(p.display(123))        # ➜ Sayı: 123
print(p.display(3.14))       # ➜ Generic: 3.14

# 🔧 METOTLAR
# - .register(type): Yeni tür için işleyici ekler
# - .dispatch(type): O tür için hangi fonksiyon kullanılacak onu verir
# - .registry: kayıtlı tüm tür-fonksiyon haritası (dict)

# ⚠️ DIKKAT
# - İlk parametre `self` olmalı
# - Metot içinde tip kontrolü yapılan parametre `self`'ten sonra gelen argümandır
