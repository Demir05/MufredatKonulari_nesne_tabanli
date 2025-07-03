
# ---------------------------------------------------------------
# 🧠 @property — Tanımsal & Kavramsal Açıklama
# ---------------------------------------------------------------
from inspect import getsource, Signature


# 🎯 Tanım:
#   @property, bir methodu "sanki bir attribute gibi" kullanmamızı sağlayan yapıdır.
#   Yani: obj.method() yerine ➝ obj.method gibi erişim yapılır.
#   Bu, Python’un descriptor protokolünü kullanan bir syntactic sugar’dır.
#       synactic sugar: Syntactic sugar, programlama dillerinde, var olan bir davranışı daha sade, anlaşılır veya yazması kolay hale getiren özel bir sözdizimidir.
#       Aslında yapabileceğin bir şeyi, daha güzel görünsün diye başka bir şekilde yazmana izin verir.
#       Şeker eklemek gibi: işlev değişmez, ama kullanım daha keyifli olur.


# ---------------------------------------------------------------
# ✅ NEDEN KULLANILIR?
# ---------------------------------------------------------------

# 1️⃣ Fonksiyon gibi çalışan özellikler tanımlamak (hesaplanabilir değerler)
# 2️⃣ Gerçek attribute değil ama dıştan öyleymiş gibi göstermek (encapsulation)
# 3️⃣ Atama ve silme işlemlerinde özel kontrol davranışı tanımlamak

# ---------------------------------------------------------------
# ⚙️ @property (getter)
# ---------------------------------------------------------------

# @property dekoratörüyle tanımlanan method, nesne üzerinden çağrıldığında
# sanki bir değişken gibi davranır. Ama aslında bu bir fonksiyon çağrısıdır.
# Bu fonksiyon → ilgili attribute’un değerini döner.
# ➜ __getattr__'a benzer ama sadece belirli attribute için geçerlidir
# ➜ Örneğin: obj.ad  →  self._ad gibi içsel veriyi döndürür

# Örnek tanım:
# @property
# def ad(self):
#     return self._ad

# Kullanım:
# kisi.ad  ←  arka planda kişi.ad() gibi çalışır ama parantezsizdir.

# ---------------------------------------------------------------
# ⚙️ @<isim>.setter
# ---------------------------------------------------------------

# Bu decorator, @property ile tanımlanmış bir özelliğe değer atandığında
# çalışacak olan fonksiyonu tanımlar.
# ➜ __setattr__ gibi ama sadece o attribute’a özeldir
# ➜ Değer doğrulama, filtreleme gibi kontroller yapılabilir

# @ad.setter
# def ad(self, yeni_ad):
#     self._ad = yeni_ad

# Kullanım:
# kisi.ad = "Ahmet"  ←  setter tetiklenir ve kontrol yapılabilir

# NOT:
# setter fonksiyonu, getter’la aynı isimde olmalı (ad/ad.setter gibi)

# ---------------------------------------------------------------
# ⚙️ @<isim>.deleter
# ---------------------------------------------------------------

# Bu decorator, del obj.x şeklinde çağrıldığında çalışacak olan methodu tanımlar.
# ➜ __delattr__ gibi ama yine sadece belirli attribute için geçerlidir
# ➜ Veriyi silme, kaynak boşaltma işlemleri yapılabilir

# @ad.deleter
# def ad(self):
#     del self._ad

# Kullanım:
# del kisi.ad  ←  bu işlemle örneğin attribute'u silinir veya dummy yapılabilir
#--------------------------------------------------------------
# 🎯 SONUÇ:
# @property sistemindeki getter/setter/deleter yapıları,
# __getattr__, __setattr__, __delattr__'ın nokta atışı versiyonlarıdır.
# Yani sadece belirli bir attribute için geçerli ve kontrollüdür.

# ---------------------------------------------------------------
# 🧱 Genel Yapı:

# class Nesne:
#     def __init__(self):
#         self._x = 0

#     @property
#     def x(self):      # getter
#         return self._x

#     @x.setter
#     def x(self, val): # setter
#         self._x = val

#     @x.deleter
#     def x(self):      # deleter
#         del self._x

# ---------------------------------------------------------------
# 🧠 SONUÇ:

# - @property, OOP'de "controlled access" sağlamanın en Pythonic yoludur.
# - Getter/setter/deleter yöntemlerini ayrı ayrı kodlamak yerine
#   tek bir isim altında çoklu davranış tanımlamayı sağlar.
# - Hem encapsulation(gerçekten attribute değil ama dışardan öyle gibi göstermek) sağlar, hem de temiz API görünümü sunar.
# - Kullanıcıdan fonksiyon gibi görünmez, ama kontrol tamamen sende olur.


# ---------------------------------------------------------------
# 🏗️ Python'un built-in property sınıfının simülasyonu
# ---------------------------------------------------------------


class MyProperty:

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        # fget → getter fonksiyonu (self.ad gibi çağrıldığında çalışacak)
        # fset → setter fonksiyonu (self.ad = ... yazıldığında çalışacak)
        # fdel → deleter fonksiyonu (del self.ad yapıldığında çalışacak)
        # doc  → property hakkında açıklama, help() çıktısı için
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or (fget.__doc__ if fget else "")
        self.fget is not None and  print(f"[LOG] >>> fget Function name is {fget.__name__}")

    def __get__(self, instance, owner):
        # instance → sınıfın örneği (self)
        # owner    → sınıfın kendisi
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        print(f"[LOG][__get__ speaking] >>> fget Function name is {self.fget.__name__} instance value is {instance } and returning")
        return self.fget(instance)

    def __set__(self, instance, value): # admin.user = "ozan" -> instance= user, value= "ozan",
        if self.fset is None:
            raise AttributeError("can't set attribute")
        print(f"[LOG][__set__ speaking] >>> fset Function name is {self.fset.__name__} instance is {instance} and returning")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        f"[LOG][__delete__ speaking] >>> fdel Function name is {self.fdel.__name__} and returning"
        self.fdel(instance)

    def getter(self, fget):
        # .getter() dekoratörü → yeni MyProperty döndürür
        print(f"[LOG][getter spech] >>> fget Function name is {fget.__name__}")
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        # .setter() dekoratörü → yeni MyProperty döndürür
        print(f"[LOG][setter spech] >>> fset Function name is {fset.__name__}")
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        # .deleter() dekoratörü → yeni MyProperty döndürür
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


class Kisi:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"

     # show = Myproperty(show) -> Myproperty.__init__(self, fget=None, fset=None, fdel=None, doc=None): >>> burda fget = show olur
    @MyProperty
    def ad(self):
        return self.__getattribute__("name")

    @ad.setter
    def ad(self, new_value):
        self.name = new_value



kisi = Kisi("demir")

print(kisi.ad)
print("deneme",(myp:=kisi.__class__.__dict__["ad"]).__class__.__dict__["getter"].__call__(myp,myp.fget)                                                                                                                                                                                                                                                                                                                                                  )
# 🔍 1) Kisi sınıfındaki 'ad' attribute'una erişiyoruz
# Bu bir @property ile tanımlanmış ve descriptor objesi (property) döndürür
myp = kisi.__class__.__dict__["ad"]  # <property object>
#   → type(kisi).__getattribute__(kisi,"ad"): attibute erişimi davranışsal bir işlem olduğundan dolayı,kisi'nin ait olduğu sınıf çağrılır
#   → Çünkü davrnaışsal işlemler nesnesin,ait olduğu sınıf tarafından yönetilir bu "örnekleme" sonucu oluşan darvanışsal bir işlemdir

# 🔍 2) property sınıfının getter metoduna ulaşıyoruz
# type(myp) == <class 'property'> olduğundan dolayı doğrudan dict'ten alabiliyoruz
getter_func = type(myp).__dict__["getter"]  # <function property.getter>
#   → Bulunan "getter", descriptor protokolüne göre çözümlenmez çünkü zaten bir bound_method döner dolasıyla __call__ ile çağrılması yeterlidir

# 🔍 3) getter() fonksiyonu aslında yeni bir property nesnesi döndürür
# self = myp (property objesi), fget = myp.fget (orijinal getter fonksiyonu)
# Bu sayede zincirleme yapı kurulur ama aynı getter fonksiyonuyla
new_prop = getter_func.__call__(myp, myp.fget)
#   → burda bound method olan getter'ı çağırdık çünkü getter,bir attribute methoddur normal attribute değil bu nedenle erişildiğinde bound method döner
#   → aynı zamanda fget parametresine myp.fget verdik orjinal getter fonksiyonu burda type(myp) vermek hata olurdu çünkü myp,property örneği

# 🔍 4) new_prop da bir property objesi olur ve orijinal property ile birebir aynı davranır
# Çünkü aynı fget/fset/fdel fonksiyonları korunmuştur
print(new_prop.__get__(kisi, kisi.__class__))  # Orijinal getter fonksiyonu çalışır

print(myp.__dict__)
kisi.ad = "ozan"
print(kisi.ad)
print(kisi.__dict__)
# ----------------------------------------------------------
# 🎯 Python @property Mekanizmasının Nihai Özeti
# ----------------------------------------------------------

# ✅ 1. Temel: property, aslında bir descriptor'dur
#    Yani: __get__, __set__, __delete__ methodlarını içerir

# obj.ad            → property.__get__() çağrılır
# obj.ad = "ali"    → property.__set__() çağrılır
# del obj.ad        → property.__delete__() çağrılır

# ----------------------------------------------------------

# ✅ 2. @property dekoratörü → sadece şekerli bir tanımdır
#    Aslında: ad = property(ad) gibi çalışır
#    Yani: fonksiyonu fget olarak saklar

# @property
# def ad(self):      ⟶ bu fonksiyon "getter"dır
#     return self._ad

# ad = property(fget=ad)  ⟶ işte tam bu olur

# ----------------------------------------------------------

# ✅ 3. .setter(), .getter(), .deleter() → sadece YENİ property objesi döner
#    Bunlar instance method'lardır (yani self ile çağrılır)
#    Amaç: mevcut fget/fset/fdel değerlerini koruyarak bir yenisini döndürmek

# def setter(self, fset):
#     return type(self)(self.fget, fset, self.fdel, self.__doc__)

# 👉 burada type(self) → property sınıfını çağırır
# 👉 self.fget → eski getter korunur
# 👉 fset → yeni setter fonksiyonu

# ----------------------------------------------------------

# ✅ 4. .getter()/.setter() kullanımı zorunlu değildir
# Sadece:
# - property'yi sonradan parçalı kurmak istediğimizde
# - veya mevcut bir property objesini güncellemek istediğimizde
# - veya bir setter ya da deleter eklemek istediğimizde kullanılır

# ----------------------------------------------------------

# ✅ 5. Kullanıcı açısından:
# obj.ad      → getter
# obj.ad = x  → setter
# del obj.ad  → deleter

# Ama içeride olan:
# obj.__class__.__dict__["ad"].__get__(obj, type(obj))
# ⟶ self.fget(obj)

# obj.__class__.__dict__["ad"].__set__(obj, val)
# ⟶ self.fset(obj, val)

# obj.__class__.__dict__["ad"].__delete__(obj)
# ⟶ self.fdel(obj)

# ----------------------------------------------------------
# 🧠 Sonuç:
# property → sadece organize edici bir araç
# esas iş → __get__, __set__, __delete__ ile descriptor sisteminde
# ve .getter()/.setter()/.deleter() → sadece yeni instance döndürerek
# fonksiyon zincirini temiz bir API ile tanımlamamızı sağlar ayrıca bu instance method'lar birer güvenlik mekanizmasıdırlar
# ----------------------------------------------------------

class Settings:
    def __init__(self, **opts):
        self.setting = opts

    @property
    def options(self):
        return self.setting

    @options.setter
    def options(self, new_option):
        print(f"eklenen yeni ayar >>> {new_option}")
        self.setting.update(new_option)


settings_object = Settings(max_fps = 60)

print(settings_object.options) # {'max_fps': 60}
settings_object.options = {"Vsync":True} # eklenen yeni ayar >>> {'Vsync': True}
print(settings_object.options) # {'max_fps': 60, 'Vsync': True}

from inspect import getsource
class Log:

    def __init__(self,func):
        #name mangling
        self.__func = func

    def __call__(self, *args, **kwargs):
        print(f"[LOG] >>> func is {self.__func.__name__}")
        print(f"[LOG] >>> func source code is;\n{getsource(self.__func)}")
        result = self.__func(*args, **kwargs)
        print(f"[LOG] >>> result is {result}")
        return result

class Base:
    def __init__(self,user):
        self.__user = user

    @property
    @Log
    def user(self):
        return self.__user


    @user.setter # user değişmesi için fset gereklidir
    @Log
    def user(self, new_value):
        self.__user = new_value

class Admin(Base):

    @Base.user.getter
    @Log
    def user(self):
       return super(type(self),self).user.upper()



#----------------
admin = Admin("demir")
print(admin.user)




