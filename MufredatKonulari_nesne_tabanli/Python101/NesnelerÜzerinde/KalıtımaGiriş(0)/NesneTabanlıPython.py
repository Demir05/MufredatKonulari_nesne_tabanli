from inspect import *
# Python'da Herşey Bir Nesnedir


# Nesne: bellekte yer kaplayan ve belirli bir davranışa sahip olan her şey,nesne olarak adlandırılır python'da her şey bir nesnedir
# bir nesnenin 3 temel özelliği vardır;

# 1) kimlik(id):bellekteki konumu/adresi olmalıdır
# 2) tür(type): bir sınıfa ait olmalıdır
# 3) değer(value): nesneler,bir değer taşıyabilmelidir

print(id(str()))  # 11775216
print(type(str())) # <class 'str'>
print(str()) # ''


# Tasarımsal Amacı

# sadelik sunması: her şey aynı şekilde değerlendirilebilir
# genellik sunar: her yapı aynı kurala uyar
# güçlü soyutlama sunar: dili tek mantıkla öğrenebilirsin


# Bu Yapının Avantajları

# nesneler üzerinde işlem yapmayı genelleştirebilirsin
# tüm nesneler,birinci sınıf vatandaştırlar
# sınıflar üzerinde işlem yapabilir  hatta metaclass oluşturabilirsin
# gelişmiş programlar yazabilirsin
# python'un her şeyi nesne olarak temsil etmesi dilin tutarlığını,genişletilebilirliğini,sadeceliğini ve gücünü aynı anda sağlar



# Class

# python'da class, veriyi ve bu veriye ait davranışları aynı yapı altında toplamak için vardır
# class, aynı türden nesneleri tanımlamak için kullanılan özellik ve davranış içeren özel bir nesnedir
# bu,programlamada nesne yönelimli yaklaşımının(oop) temelidir

# Bazı Temel Sınıflar

# type,python'da bulunan tüm sınıfların oluşturulduğu sınıf nesnesi

print(type(str))
print(type(filter))
print(type(reversed))
"""
<class 'type'>
<class 'type'>
<class 'type'>
tüm nesneler,sınıf oldukları için ve python'da bulunan sınıflar,type sınıfından türetildikleri için <class 'type'> döner
"""

# function: def veya lambda ile tanımlanmış olan user-definded fonksiyonlar,function sınıfının örneğidirler
# function sınıfını,kullanıcı doğrudan göremez yalnızca fonksiyon tanımlamada python tarafından otomatik oluşturur

def merhaba():
    pass

print(type(merhaba)) # <class 'function'>

l = lambda:print(...)

print(type(l)) # <class 'function'>

# builtin_function_or_method: python'da C dilinde yazılmış olan builtin fonksiyonların miras aldığı bir sınıftır
# bu sınıf C dilinde yazıldığı için kaynak kodlarına erişilemez dolaysısyla builtin fonksiyonlar da bu sınıftan örnek aldıkları için hiç bir builtin fonksiyonun kaynak kodlarına erişilemez
# builtin_function_or_method sınıfı,builtin fonksiyonların performans açısından kritik olması ve bu fonksiyonların mümkün oldukça hızlı çalışması gerekmesi için oluşturulmuştur

print(type(max)) # <class 'builtin_function_or_method'>
print(type(sorted)) # <class 'builtin_function_or_method'>


# Module: python'da bir .py dosyasını veya dış kütüphaneyi import ile içeri aktardığında bu yüklenen şey bir modül nesnesi olur
# ve modül nesneleri module sınıfından türemişlerdir
# module sınıfı,python'da birden fazla değeri(str,int,function) düzenli bir şekilde taşıyan kapsayıcılardır bu kapsayıcılar fonksiyon değillerdir

import math

print(type(math)) # <class 'module'>


# Generator Sınıfı:python'da yield kullanan veya expression ile oluşturulan nesnelerin miras aldığı sınıftır
# bu sınıflar __next__(),__iter__(),.send(),.throw(),.close() gibi metodlara sahiptirler
# generatator sınıfı,nesnenin kendisini kontrol edebilen bir sınıftır
from collections.abc import Generator

def coroutine() -> Generator[int,None,None]:
    yield 1
    yield 2
    yield 3

print(type(coroutine)) # <class 'function'>
# şuan coroutine fonksiyonun türü bir fonksiyon,çağrılması gerek

cor = coroutine()

print(type(cor)) # <class 'generator'>

gene = (i for i in range(1))

print(type(gene))  # <class 'generator'>



# Sınıf ve Fonksiyon için tasarımsal farklar


# python'da bir yapı: yeni bir davranış modeli üretmek istiyorsa,içinde durumunu(state) tutuyorsa,çağrıldığında yeni bir nesne döndürüyorsa bu yapı Class(sınıf) olur
# sınıflar,bir davranışı modellemek için oluşturulur ve çağrıldıklarında yeni bir nesne üretirler

# eğer python'da bir yapı: sadece bir işlem yapacaksa,girilen veriyi dönüştürüp geri verecekse,state(durum) tutmuyorsa bu yapı fonksiyon olur
# fonksiyonlar,anlık görevler için çağrılır çalışırlar sonra sonra ererler ve doğrudan bir sonuç döndürürler


# örnekler;

# reversed() bir sınıftır çünkü bir nesne döner,bu nesne tersten dolaşılabilir ve durum(state) tutar

# sorted() bir fonksiyondur çünkü verilen bir iterable'dan bir liste döner,bu işlem tek seferliktir,durum tutmaz,çalışır -> sonucu üretir-> işlevi biter
""""""
"""
İsim               Tür          Açıklama
------------------ ------------ ------------------------------
reversed           Sınıf        Sınıf (iterator üretir)
sorted             Fonksiyon    Fonksiyon (liste döner)
range              Sınıf        Sınıf (lazy iterable)
enumerate          Sınıf        Sınıf (iterator döner)
zip                Sınıf        Sınıf (çoklu iterable)
iter               Fonksiyon    Fonksiyon (iterator üretir)
next               Fonksiyon    Fonksiyon (bir sonraki eleman)
map                Sınıf        Sınıf (lazy map)
filter             Sınıf        Sınıf (koşullu filter)
lambda             Fonksiyon    Fonksiyon (anonim)
tee                Fonksiyon    Fonksiyon (çoklayıcı iterable üretir)
sum                Fonksiyon    Fonksiyon (toplam)
max                Fonksiyon    Fonksiyon (en büyük)
min                Fonksiyon    Fonksiyon (en küçük)
len                Fonksiyon    Fonksiyon (uzunluk)
abs                Fonksiyon    Fonksiyon (mutlak değer)
list               Sınıf        Sınıf (dizi)
tuple              Sınıf        Sınıf (sabit dizi)
str                Sınıf        Sınıf (metin)
dict               Sınıf        Sınıf (anahtar-değer)
set                Sınıf        Sınıf (kümeler)
frozenset          Sınıf        Sınıf (değiştirilemez küme)
Counter            Sınıf        Sınıf (sayıcı dict)
defaultdict        Sınıf        Sınıf (varsayılan dict)
OrderedDict        Sınıf        Sınıf (sıralı dict)
namedtuple         Sınıf        Fonksiyon → Sınıf üretir (tuple-türevi)
count              Sınıf        Sınıf (sonsuz sayaç)
cycle              Sınıf        Sınıf (sonsuz döngü)
repeat             Sınıf        Sınıf (tekrarlayıcı)
isfunction         Fonksiyon    Fonksiyon test fonksiyonu
isbuiltin          Fonksiyon    Built-in kontrolü
isclass            Fonksiyon    Sınıf kontrolü
isgeneratorfunction Fonksiyon    Generator fonksiyon mu?
"""



