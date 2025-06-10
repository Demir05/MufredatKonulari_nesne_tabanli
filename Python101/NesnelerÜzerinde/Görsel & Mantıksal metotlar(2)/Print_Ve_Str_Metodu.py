# ---------------------------------------
# print() Fonksiyonu Tanımı
# ---------------------------------------

# print(), Python'da ekrana çıktı vermek için kullanılan yerleşik (built-in) bir fonksiyondur.
# Herhangi bir nesneyi, yazılabilir (string) hale getirip standart çıktıya (genellikle ekrana) yazar.

# Sözdizimi (Signature):
# print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)

# Parametreler:
# *objects : Yazdırılacak bir veya birden fazla nesne. Aralarında virgül koyarak birden fazla yazılabilir.
# sep      : Birden fazla nesne varsa, aralarına hangi karakter konulacağını belirtir (varsayılan: ' ' boşluk).
# end      : Çıktının sonunda ne yazılacağını belirler (varsayılan: '\n' yani satır sonu).
# file     : Çıktının yazılacağı hedef. Varsayılan olarak sys.stdout (ekran).
# flush    : True verilirse çıktı buffer’ı hemen temizlenir (anında yazılır), varsayılan False.

# Örnek:
# print("Merhaba", "Dünya")       → Merhaba Dünya
# print("a", "b", sep="-")       → a-b
# print("bitti", end="!")        → bitti!

# flush parametresi;
"""
import time 

for k in "demir ariman":
    print(k,flush=True,end="")
    time.sleep(0.2)"""



# ---------------------------------------
# __str__() Metodu Tanımı
# ---------------------------------------

# __str__() metodu, bir nesnenin insan tarafından okunabilir (user-friendly) string temsiliğini döner.
# print(obj) çağrıldığında Python, otomatik olarak obj.__str__() metodunu çağırır.

# __str__() metodu, nesneyi yazdırılabilir hale getirmek için özelleştirilir.
# Genellikle kullanıcıya anlamlı bilgi vermesi için tanımlanır.

# Sözdizimi:
# def __str__(self) -> str:
#   return f"..."

# Bu metod, daima string döndürmelidir (aksi takdirde TypeError oluşur).

# Örnek:
# class Kisi:
#     def __init__(self, ad):
#         self.ad = ad
#     def __str__(self):
#         return f"Kişi: {self.ad}"

# k = Kisi("Ali")
# print(k)         → Kişi: Ali
# Çünkü: → k.__str__() çağrıldı


# 📌 __str__() Metod Çözümleme Zinciri

# ==========================================================
# 🔹 1) ÖRNEK DÜZEYİNDE (__str__ → object.__str__ ile çözülür)
# ==========================================================

# Diyelim ki bir sınıf tanımladık:
class Araba:
    pass

a = Araba()  # Örnek oluşturduk

# ➤ Şimdi: print(a) → str(a) → a.__str__()

# 🔄 Metod çözümleme şu adımlarla olur:

# 1) Python `str(a)` dediğinde → `a.__str__()` çağrılmak istenir
# 2) Bu bir metod çağrısı olduğu için → attribute erişimi yapılır:
#    → type(a).__getattribute__(a, '__str__')

# 3) __getattribute__ çalışır, sırasıyla MRO zincirine göre '__str__' aranır:
#    → önce Araba.__dict__['__str__'] var mı bakılır
#    → yoksa Araba.__bases__ → object.__dict__['__str__'] bulunur

# 4) object.__str__ → bir descriptor (method-wrapper)
#    → __get__ protokolü uygulanır: object.__str__.__get__(a, Araba)
#    → bound method döner

# 5) bound method çağrılır: object.__str__(a)

# ✅ Sonuç: "<__main__.Araba object at 0x...>" gibi bir string döner

print(
    a.__class__.__mro__[1].__dict__["__str__"].__get__(a,Araba).__call__() # <__main__.Araba object at 0x000001FBFFF1AAD0>
)

# ==========================================================
# 🔹 2) SINIF DÜZEYİNDE (__str__ → type.__str__ yok → type.__repr__ kullanılır)
# ==========================================================

# Şimdi: print(Araba) → str(Araba) → Araba.__str__()

# 🔄 Metod çözümleme şu adımlarla olur:

# 1) Python `str(Araba)` dediğinde → Araba.__str__() çağrılmak istenir
# 2) Bu bir metod çağrısıdır, dolayısıyla yine attribute erişimi yapılır:
#    → type(Araba).__getattribute__(Araba, '__str__')

# 3) __getattribute__ çalışır, 'Araba' bir sınıf olduğundan type sınıfı kullanılır
#    → type.__dict__['__str__'] aranır

# 4) ❌ type sınıfında '__str__' bulunmaz → Python fallback yapar
# 5) Fallback → type.__repr__(Araba) çağrılır
#    → type.__repr__ bir descriptor’dır → __get__ uygulanır
#    → bound method alınır: type.__repr__.__get__(Araba, type)
#    → bound method çağrılır: type.__repr__(Araba)

# ✅ Sonuç: "<class '__main__.Araba'>" gibi bir çıktı döner


# ==========================================================
# 📝 NOT:
# - Örnekler object sınıfından miras aldığı için object.__str__ kullanılır
# - Sınıflar ise type sınıfının örneği olduğu için __str__ çözümlemesi oradan başlar
# - type sınıfında __str__ olmadığı için Python otomatik olarak type.__repr__'a geçer


# ---------------------------------------
# __str__() vs __repr__() Karşılaştırması
# ---------------------------------------

# __str__ → Kullanıcı dostu çıktı sağlar, kullanıcıya yönelik
# __repr__ → Geliştiriciye yönelik çıktı sağlar, genellikle "yeniden oluşturulabilir (eval ile)" bir formatta

# Sıralama: Python önce __str__() metoduna bakar
# Eğer __str__ yoksa, __repr__() çağrılır

# class Araba:
#     def __repr__(self):
#         return "Araba('BMW')"
#     def __str__(self):
#         return "BMW Araba"

# print(Araba()) → "BMW Araba"
# del Araba.__str__
# print(Araba()) → "Araba('BMW')"

# Sonuç:
# __str__ yoksa, __repr__ kullanılır
# __repr__ her zaman tanımlı olmalı, __str__ ise kullanıcı arayüzü için özelleştirilir

class Demir:

    def __init__(self):
        self.isim = "demir"
    def __str__(self):
        return f"{self.__class__.__name__}"

d = Demir()

print("__str__" in vars(object))
print(d)
print(Demir.__str__) # <function Demir.__str__ at 0x000001FBFFF156C0>

print(
    str.__class__.__dict__["__repr__"].__get__(str,type).__call__(), # <class 'str'>
    str.__class__.__mro__[1].__dict__["__str__"].__call__(str), # <class 'str'>
    object.__dict__["__str__"].__call__(str) # <class 'str'>
)


print(
    a.__class__.__bases__[0].__dict__["__str__"].__call__(a), # <__main__.Araba object at 0x000001FBFFF1AAD0>
    a.__class__.__bases__[0].__dict__["__str__"].__class__, # <__main__.Araba object at 0x000001FBFFF1AAD0>,
    a.__class__.__bases__[0].__dict__["__str__"].__get__(a,type(a)).__call__(), # <__main__.Araba object at 0x000002AEF9C6AB10>
    
)

print(
    a.__class__.__bases__[0].__dict__["__repr__"].__class__ # <class 'wrapper_descriptor'>
)


print(
    a.__class__.__bases__[0].__dict__["__repr__"].__get__(a,type(a)).__call__(), # <__main__.Araba object at 0x00000206BE37AB90>
        a.__class__.__bases__[0].__dict__["__repr__"].__call__(a) # <__main__.Araba object at 0x00000206BE37AB90>

)