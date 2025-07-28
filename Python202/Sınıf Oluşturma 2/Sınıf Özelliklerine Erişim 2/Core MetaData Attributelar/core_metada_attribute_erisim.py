# ------------------------------------------------------------
# 📌 ÖZELLİKLERİN DAVRANIŞI
# ----------------------------

# Core MetaData'lar, Getset descriptor olarak type sınıfında bulunurlar.
# Dolayısıyla sınıf oluşturulma sürecinde(hem namespace["__module__"] = x ve class body'de __module__ = x)
# descriptor protokolü uygulanır yani;

class Meta(type):
    def __new__(cls, name, bases, namespace,**kwargs):
        namespace["__module__"] = "deneme"
        result = super().__new__(cls,name,bases,namespace,**kwargs)
        # tam burda, type.__new__() çağrısında descriptor protokolü uygulanır senin verdiğin veri,__set__ ile
        # descriptor'e yazılır.
        return result

# Descriptor protokolü,sadece sınıf oluşturulma sırasında namespace üzerinden değil class body'de tanımlanarak da olur.
# daha sonrasında type.__new__ ile sınıf oluşturulurken python, yine descriptor protokolü uygulanır.

class A:
    __module__ = "deneme"
    # bu yazımda tamamen geçerlidir

# __qualname__,__modulue__,__name__,__doc__ gibi Core MetaData'lar ReadOnly Descriptor değillerdir
# yani set edilebilirler,bu işlemde bu attribute'lar silinmez ama içerikleri değişebilir.

A.__class__.__dict__["__module__"].__set__(A,"yeni")
# burda unbound olan ve Getset Descriptor olan __module__ attribute'Unu A sınıfına bağlayarak set ettik

print(A.__module__) # yeni

# __module__ ve __doc__ attribute'ları sınıfın sözlüğünde ayrıca yer alırlar bu şunu açıklar;
#   1) obj.__module__/__doc__ kullanıldığında sınıfın sözlüğündeki attribute döner ama descriptor protokolü sözkonusu değildir
#   2) MyClass.__module__/__doc__ kullanıldığında descriptor protokolu uygulanır çünkü Descriptor önceliklidir
#   bu sayede bu attribute'lar hem örneklerde hem de sınıf üzerinden kullanılabilir