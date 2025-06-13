# 🧾 repr: Nesnelerin Temsili

# 📌 Repr, bir nesnenin geliştirici odaklı (resmi) temsili anlamına gelir.
# Python'da her nesne, string'e dönüştürülebilir. Bu string temsili, iki ana şekilde olabilir:
#   1) kullanıcıya gösterilecek biçim (→ str)
#   2) geliştiriciye/derleyiciye yönelik biçim (→ repr)

# Repr'ın temel amacı: bir nesneyi **yeniden oluşturulabilir** veya **debug edilebilir** şekilde yazdırmaktır.
# >>> x = [1, 2, 3]
# >>> repr(x)
# '[1, 2, 3]'

# Repr ifadesi sayesinde:
# - nesneleri debugging sırasında kolayca analiz edebiliriz
# - etkileşimli kabukta (REPL) doğru çıktı alabiliriz
# - loglama, hata mesajı gibi durumlarda daha anlamlı çıktılar üretebiliriz

# 🔍 print(obj) → str() çağrılır, ama doğrudan >>> obj yazarsan → repr() çağrılır.

# 📌 __repr__() Metodu:
# Repr davranışını kontrol etmek istiyorsan, sınıfına __repr__() metodunu tanımlarsın.
# Bu metodun amacı: sınıfın örneği için açıklayıcı, yeniden oluşturulabilir bir string döndürmektir.

# 🧠 NOT:
# - Eğer __repr__() yoksa, varsayılan olarak object veya type sınıfından gelen:
#   → <__main__.SınıfAdı object at 0x...> gibi bir çıktı alınır.
# - Bu pek bilgilendirici değildir, override ederek özelleştirmek yaygın bir uygulamadır.

# 🧪 Sözdizimi:
# def __repr__(self) -> str:
#     return f"SınıfAdı(attr1={self.attr1}, attr2={self.attr2})"

# 🎓 REPR’ın temel amacı: objeyi **geliştirici açısından anlamlı ve doğru** bir şekilde temsil etmektir.
# Bu temsili string çıktılar genellikle bir nesnenin "yeniden yaratılabilir hali" gibi düşünülür.

# ➕ BONUS:
# eval(repr(obj)) → objeyi tekrar oluşturmaya çalışabilir (her zaman değil, ama ideal hedef budur).

# ✅ O halde __repr__() yazmak, sınıf tasarımı açısından oldukça önemlidir.


# 🔁 __repr__() METODUNUN METOD ÇÖZÜMLEME ZİNCİRİ (örnek + sınıf düzeyi)

# __repr__() → bir nesnenin (veya sınıfın) "resmi" string temsili için kullanılır.
# Bu metod çağrıldığında Python, bir attribute erişimi algılar ve __getattribute__ zinciri başlatılır.

# ⬇️ ÖRNEK DÜZEYİ: repr(obj)
# 1) Python → repr(obj) çağrılır
# 2) → type(obj).__getattribute__(obj, '__repr__')
# 3) → obj.__class__.__dict__['__repr__'] aranır
#     → yoksa __mro__ zincirinde (base class → object) aranır 
# 4) → object sınıfında bulunan metod,Descriptor'dur python,bound method elde etmek için descriptor protokolü uygulanır
#     → type(obj).__dict__['__repr__'].__get__(obj, type(obj)) burda __get__ metodu, obj'ye bağlanır ve bound method elde edilir
# 5) → elde edilen bound method çağrılırır 
#     → bound_method_.__call__() 
# sonuç olarak string ifade döner(expressin)
 
# ⬇️ SINIF DÜZEYİ: repr(Sınıf)
# 1) Python → repr(Sınıf) çağrılır
# 2) → type(Sınıf).__getattribute__(Sınıf, '__repr__')
# 3) → Sınıf.__dict__['__repr__'] aranır  bulunan metod,Descriptor'dur python,bound method elde etmek için descriptor protokolü uygulanır
#    -> type(Sınıf).__dict__['__repr__'].__get__(Sınıf, type(Sınıf)) bunun sonucunda bound method elde edilir
# 4) → elde edilen bound method çağrılırır
#     → yoksa type → object zincirinde aranır
# 5) → Bound method,çağrılırır
#     → bound_method.__cal__(*args,**kwargs)
# 6) → string çıktı döner

# 🧠 NOT:
# - Hem objeler hem sınıflar, __repr__ erişiminde __getattribute__ zinciri başlatır.
# - Python her zaman attribute erişimini, type(obj).__getattribute__ ile başlatır.
# - type sınıfı bu davranışların merkezidir çünkü sınıfların kontrolünü sağlar.

# 🎓 Eğer hiçbir __repr__ tanımı bulunamazsa, object veya type  sınıfındaki __repr__ çağrılır:
# → <__main__.SınıfAdı object at 0x7fd5c...> gibi bir varrsayılan çıktı

class Sinifım:

    def __init__(self):
        self.attrs = []

    def __repr__(self):
        return f"{type(self).__name__}({self.__dict__!r})"

s = Sinifım()

print(repr(s)) # Sınıfım({'attrs': []})
print(s) # Sınıfım({'attrs': []})
# Bunun nedeni: print fonksiyonu sınıfta bulunan __str__() metodunu çağırır eğer bulamazsa __repr__ metodunu çağırır
# hatırlarsan literal olmayan veri yapılarını doğrudan print ile standart kontrol akışına yazdırdığın zaman python,otomatik olarak __repr__() metodunu çağırıyordu


print(
    object.__dict__["__repr__"].__call__(s), # <__main__.Sinifım object at 0x0000013AFC26EAD0>
    # bu __repr__, non-data descriptor'dur python,doğruca __call__ metodunu uygular

    object.__dict__["__repr__"].__get__(s,Sinifım), # <method-wrapper '__repr__' of Sinifım object at 0x000001634026EB10>
    # non-data descriptor olduğundan dolayı __get__ kullanabiliriz ama python bu metodu böyle çözümlemez

    object.__dict__["__repr__"].__get__(s,Sinifım).__call__() # <__main__.Sinifım object at 0x000002868AE6EB50>
)