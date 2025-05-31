# Class


# python'da class, veriyi ve bu veriye ait davranışları aynı yapı altında toplamak için vardır
# class, aynı türden nesneleri tanımlamak için kullanılan özellik ve davranış içeren özel bir nesnedir
# bu,programlamada nesne yönelimli yaklaşımının(oop) temelidir

# teknik olarak class,type sınıfının örneğidir ve __new__() + __init__() metodları ile yeni bir nesne üretir

# sözdizimi;

class ClassName:

    def __init__(self):
        pass

"""
class: class,yeni bir şablon oluşturmanı sağlar(yani class -> şablon oluşturucu) bu şablon,daha sonra nesneler üretmek için kullanılır 

ClassName: ClassName,burda şablon adıdır, tip tanımıdır

def: sınıf içinde tanımlanan çağrılabililir bir bloktur bu bloğun adı __init__'idir 

self: self,bir sınıfın içindeki metodlarda o sınıfın oluşturduğu nesnenin kendisini temsil eder 
sınıflar,fonksiyonlar gibi bir işlemi gerçekleştirip sonrasında kapanmazlar programın çalışma süresi boyunca yaşarlar 
bu durumda,bu sınıftan miras gelen her alt nesneye farklı davranışlar sunmak için kullanılır çünkü her nesnenin durumu farklı olabilir 
metodların,hangi nesne üzerinde çalıştığını bilmesini sağlar ve python sınıf çağrısında self parametresini kendisi koyar 
ve self,geleneksel bir isimdir sabit bir isim değildir ama programlama caimasında herkes tarafından anlaşılabilir
"""


# Sınıf çağırma

