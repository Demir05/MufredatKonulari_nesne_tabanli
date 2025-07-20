# Konu: Descriptor sınıflarında instance method'lara erişim ve argüman geçişinin mantığı
from functools import update_wrapper, wraps


# 🔹 Descriptor protokolü sayesinde bir attribute’a erişim kontrol edilebilir.
# 🔹 Bir descriptor, __get__ tanımlarsa: attribute erişimi sırasında çağrılır.
# 🔹 Eğer descriptor'la sarılan şey bir INSTANCE METHOD'sa (yani 'self' alıyorsa),
#    o zaman descriptor içinden bu method'u çalıştırmak için instance'a erişmemiz gerekir.

# 🔸 Normalde methodlar instance'a bağlı olduğunda "bound method" haline gelir.
# 🔸 Ama descriptor içindeki func, unbound method’tur. Yani doğrudan self.func() çağrısı hata verir.
# 🔸 Bunun için instance'ı manuel geçirerek 'self.func(instance, *args)' gibi çalıştırmak gerekir.

# 🔸 Fakat descriptor'ın __get__'inde instance mevcuttur!
#    Bu sayede instance'ı bağlayan bir lambda fonksiyonu tanımlayarak,
#    hem method'u çağırabilir, hem de argüman geçişini sağlayabiliriz.

# 🔹 Python'da bu 'lambda' ifadesi bir closure'dır:
#    - İç fonksiyon (lambda), dış fonksiyonun local scope’una erişir
#    - Dış fonksiyon (__get__) kapandığında bile, iç fonksiyon (lambda) instance ve func’a erişmeye devam eder
#    - Böylece descriptor, method’u instance’a bağlı şekilde çağırabilir hale gelir

# 🧠 Bu mekanizma sayesinde descriptor ile hem method binding hem argüman yakalama mümkün olur.

# NOT;

# “self’e ulaşmamız __call__ ile gereksiz ve geçersiz.
# Çünkü __call__, instance method’a erişim zincirine bağlı değil.
# Static method’lar için mantıklı olur.
# Ama instance method için __call__ içinde self’e erişemeyiz.
# Unbound method olan orijinal fonksiyonu __call__ içinde instance’a bağlayamayız.”

# Descriptor sınıfı
class O:
    def __init__(self, func):
        # Bu descriptor'a sarılan method
        self.func = func

    def __get__(self, instance, owner):
        # instance yoksa (sınıftan çağrılırsa), descriptor'ın kendisini döndür
        if instance is None:
            return self

        # 🔥 Lambda bir CLOSURE oluşturur:
        # instance ve func bağlanır, böylece name argümanı ile çalıştırılabilir
        return lambda name: self.func(instance, name).title()


# Kullanım sınıfı
class B:
    @O
    def selamla(self, name):
        return name


# Deneyelim:
b = B()
print(b.selamla("demir"))  # ➜ "Demir"

class O1:
    def __init__(self, func):
        self.func = func
    def __get__(self, instance, owner):
        @wraps(self.func)
        def wrapper(*args, **kwargs):
            return self.func(instance, *args, **kwargs)
        return wrapper

class B:

    @O1
    def selamla(self,name):
        """deneme"""
        return name

b = B()
print(b.selamla("demir"))
print(b.selamla.__doc__)

class O2:
    def __init__(self, func):
        self.func = func
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.func(instance)




class Bravo2:

    @O2
    def selamla(self):return "demir"

bravo = Bravo2()
print(bravo.selamla)