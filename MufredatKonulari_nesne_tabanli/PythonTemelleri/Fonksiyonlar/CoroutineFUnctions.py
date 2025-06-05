# Coroutine Functions

# coroutine functions,çalışırken yani runtime esnasında dış dünyadan veri alabilen,kendi içinde durup devam edebilen,kontrol akışlarını devredip geri alabilen
# hafif yapılı,modüler fonksiyonlara verilen özel bir isimdir
# bir fonksiyonun Coroutine fonksiyon olarak adlandırılması için yield veya yield from anahtar kelimeleri olmalıdır yani fonksiyon generator function olmalıdır
# python'daki coroutine fonksiyonlar,send() ve stop() gibi özel metodlara sahiptirler
# coroutine fonksiyonlar,çoğunlukla döngülerle birlikte kullanılır çünkü bu yapının sürekli veri alması gerekir bunuda ancak bir döngü ile yapabilir


# temel sözdizimi;

def coroutine():
    sonuc = None
    while True:
        veri = yield sonuc
        #sonuc = <expression(veri)>
# çalışma mantığı ve sırası;
# 1) coroutine() çağrılır ama bu fonksiyon bir generator üretir dolayısıyla ilk çağrıda herangi bir değer üretmez veya döndürmez
# 2) next() veya send() çağrıları ile fonksiyon,ilerler
# 3) yield satırında,yield bir statemnts olduğu için ilk olarak sağ taraf değerlendirilir sonuc değeri, dışarı döner
# 4) beklemeye geçilir
# 5) send() çağrılır ve dışardan veri alınır bu veri,veri nesnesine atanır send() fonksiyonu'da ilerletir bu durumda;
# 6) tekrar döngüye girilir ve önceki sonuc değeri,dışarı döndürülür
# 7) tekrar beklemeye geçilir
# ÖZEL DURUM: eğer fonksiyonda sonlandırıcı return varsa döngu kapatılır ve genrator biteceği için sonraki next() veya send() çağrısında StopIteration hatası alınır

def coroutine2():
    sonuc = None
    while True:
        veri = yield sonuc
        yield veri
# Çalışma mantığı ve sırasını farklarını açıklayarak bahsedelim;

# bu fonksiyonun farkı iki tane yield olması
# 1)next veya send ile generator başlatıldığında yield sonuc dışarı döner sonra beklemeye geçer
# 2) send() ile veri alındığında fonksyion ilerler
# 3) yield veri satırında veri,dışarı döner sonra ise beklemeye geçilir
# 4) bu durumda eğer send() ile veri gönderilirse bu veri boşa gider çünkü bu değer bir yere atanmıyor
# ama burda send veya next gerekli çünkü şuan fonksiyon yield veri satırında ve bunun ilerlemesi için sanki ilk çalıştırmada yaptığımız;
# next(gen) veya gen.send(None) kullanmalıyız
# 5) fonksiyon ilerler ve tekrar döngüye girer veri = yield sonuc satırında sonuc,dışarı döner ve beklemeye geçilir
# 6) İŞTE ŞİMDİ send() ile alınan veri,veri değişkenine atanır

# özet;
"""
parola = yield          # (1) → veri alımı bekler
yield parola            # (2) → dışarı veri gönderir, sonra DURUR"""

# özellikleri;

# duraklayabilirler
# devam edebilirler
# veri alabilirler
# veri verebilirler
# durumu/konumu saklar
# lazy evaluation işlemi sayesinde bellek dostudur
# runtime olarak koda dinamiklik katar yani fonksiyon çalışırken karar yapılarından etkilenip kodun davranışını değiştirerek bunu yapar

# Coroutine VS diğer yapılar

# argüman: fonksiyon başlamadan sabit bir şekilde veri alabilir runtime çalışamaz
# dekaratör: fonksiyonu sararar dinamiklik katar ama bu dinamiklik sadece fonksyiyon başlarken işe yarar runtime olarak çalışmaz
# coroutine: çift veri akışı ve runtime olarak fonksiyonu dinamiklik katar


# Kullanım Alanları;

# sürekli veri alan sistemlerde çok sık kullanılır
# etkin veri işlemde
#  komut yorumlamada
# pipeline sistemlerde
# duruma duyarlı makinelerde

# örnek 1;

def toplayacı(start):
    toplam_değer = start
    while True:
        inpu = yield toplam_değer
        toplam_değer += inpu

topla_gen = toplayacı(1)

print(topla_gen.send(None)) # ilk olarak kod satırın yield toplam_değer'i yorumlayıp hesaplaması için yaptık
# aynı zamanda yield'İn değeri olduğu içinde print ile alınan değeri döndürdük start > 1 olduğu için: # 1 yazdı

print(topla_gen.send(2)) # 3
print(topla_gen.send(3)) # 6

# örnek 2;

def harmonik_ortalama(w=None):
    from statistics import harmonic_mean
    sonuc = None
    while True:
        a,b = yield sonuc
        # açıklaması: normal olarak a,b = yield dışarıya herangi bir değer döndürmez bu nedenle send() çağrısı,
        # dışarıya None döndürür eğer send() ile dışarıya sonuç almak istiyorsan yield sonuc yapısını kullanarak,
        # bir önceki sonucu döndürmek gerekir aynısını toplayıcı fonksiyonunda yaptık

        sonuc = harmonic_mean((a,b))

ho = harmonik_ortalama()

ho.send(None) # bir önceki sonuc değerini döndürdü sonra beklemeye geçti

print(ho.send((1,3))) # 1.5  # değerler sırayıla a ve b'ye unpacikng edildi sonra kod,tekrar yield satırına gitti
# yield sonuc,sonuc değerini dışarı döndürdü ve beklemeye geçti
"""
    (1, 3) coroutine'e gönderildi

    a, b = (1, 3) → unpacking yapıldı

    harmonic_mean((1, 3)) = 1.5 hesaplandı

    sonuc = 1.5 olarak güncellendi

    Döngüye döndü ve tekrar yield sonuc satırına geldi

    yield 1.5 → dışarı döndürdü

    Durakladı ve yeni veri bekliyor
"""

print(ho.send((2,4))) # 2.6666666666666665
print(ho.send((3,5))) # 3.75

# örnek 3;

def check_password():
        parola = ""
        while True:
            parola = yield
            if len(parola) > 5:
                print("güçlü parola",parola)

            else:
                print("güçsüz parola",parola)

cp = check_password()

cp.send(None)

cp.send("demirarıman")
cp.send("de")

"""
güçlü parola demirarıman
güçsüz parola de
"""

# örnek 4

def komut():
    while True:
         kod = yield
         match kod:
           case 1:
               print("1.komut yürütüldü")
           case 2:
               print("2.komut yürütüldü")
           case _:
               print("bilinmeyen komut")

k = komut()

k.send(None)

k.send(1)
k.send(2)
k.send(3)
"""
1.komut yürütüldü
2.komut yürütüldü
bilinmeyen komut
"""

# close() METODU

# bir generator veya coroutine nesnesini dışardan güvenli bir şekilde erkenden sonlandırmak için kullanılır
# bu çağrı generator'ün bulunduğu konumda GeneratorExit adında özel bir sinyal fırlatır bu sinyalden sonra generator durur ve
# close() metodu,throw() metodu aracılığı ile GeneratorExit istisnası fırlatır bu durumda eğer generator içinde try/finally varsa
# temizlik işlemleri yapılabilir çünkü bu sinayli exception handling yapabilirsin ama bypass edemezsin(ileride anlatılcak),eğer final olarak yapılması gereken
# temizlik işleri varsa yapabilirsin

# sözdizimi gen.close() -> argüman almaz

# Neden close() Kullanılır;
# belleği serbest bırakmak için
# açık kaynakları kapatmak için
# finally garantisi
# uzun ömürlü corounter'ları kapatmak için

# close() metodu çağrıldığında python,gen.throw(GeneratorExit) işlemini yapar

# GeneratorExit: python'un close() metodunu çağrıldığında otomatik olarak fırlatırlan özel bir istisna sinyalidir
# bu sinyal bastırılmamalıdır(yakalayabilirsin ama işlem yapamazsın) çünkü bu sinyal: "artık döngü bitilirsin "demektir ve bastırmaya çalışıldığında;
# python interpreter'ine karşı gelmiş olursun ve RuntimeError hatası alırsın
# GeneratorExit'İn istisna olmasının nedeni de program kontrolünü restore etmek için kullanılır kullanıcı,bu sinyali görmezden gelemez

k.close() # k coroutine fonksiyonu kapatıldı

def f():

    try:
        yield "Çalışıyorum"

    finally:
        print("temizlik işlemleri...")

gen = f()

print(next(gen))
input()
# burda input() kullandık çünkü pycharm,otomatik olarak GeneratorExit sinyali fırlatıyor
"""
Çalışıyorum
a
temizlik işlemleri...
"""
gen.close() # artık gen coroutine fonksiyonu kapatıldı terkar next kullanımında;

try:
    next(gen)
except StopIteration: print("StopIteration sinyali alındı") # StopIteration sinyali alındı

# örnek 2;

def f():
    try:
        while True:
            yield "Çalışıyorum"
    except GeneratorExit:
        yield 1

gen = f()

print(next(gen))
try:
    gen.close()
except RuntimeError: # runtime hatası alındı
    print("runtime hatası alındı")
input()
# burda runtime hatası alınır çünkü close() metodu,thorw(GeneratorExit) fırlatacak ve sen bunu yakalayıp ignore ederesen hata alırsın


# throw() METODU

# throw() metodu,Çalışma(runtime) esnasında generator veya coroutine içersine dışardan istisna fırlatmanı sağlayan bir metoddur
#bu metodun raise'den farkı raise,içerden istisna fırlatırken throw(),dışardan içeriye istinsa fırlatmanı sağlar

# hata similasyonu yapmak için kullanılır genelde

# throw metodu,otomatik olarak python tarafındanda kullanılır örneğin: close() ile fonksiyonu sonlandırırken python;
# thow(GeneratorExit) metodu sayesinde GeneratorExit sinyalini fırlatır

# bu fırlatılan istisnayı,coroutine fonksiyonunda tanımlanan except bloğu yakalayabilir bu sayede prgramın davranışını değiştirebilirsin
# eğer except bloğu tanımlı değilse;python,bu hatayı dışarı fırlatır ve coroutine derhal sonra erer(çöker doğrusu)

# NOT: throw() metoduyla,bir coroutine'e istisna göndermek istiyorsan coroutine'nin aktif olması gerekmetedir
# yani kodun,yield satırına gelmesi gerek ancak yield satırında hata yakalama yapılabilir ayrıca bu yield,try bloğunun altında tanımlanmalıdır(try,aktif olmalı)
"""try:
    yield from range(1,20)
"""
# eğer generator,başlatılmadan  throw() ile  hata gönderirmek istenirse bu hata ilk satırdan doğruca dışarı fırlatılır ve;
# bu durumda hata yakalama yapılamaz fonksiyon,çöker derhal çalışmasına son veririr
# ayrıca except bloğununda yield yoksa,generator biteceği içinde hata sonrasında StopIteration hatası alınır


# sözdizimi: gen.throw(exc_type,exc_instance=None,traceback=None)
# exc_type: fırlatılcak olan istisna sınıfı(TypeError gibi hata sınıfı olmalıdır ve zorunludur)
# exc_instance: (opsiyonel) hata sınıfından bir örnek,sınıf olamaz  Not: throw(exc_instance) -> sadece türü eşleştirir ama örneği yani mesajı erişilebilir hale getirmez
# # bu durumda except bloğunda takma isim yani as kullanmalısın
# traceback: (opsiyonel) özel traceback objesi

def coroutine():
    try:
        while True:
            yield "demir"
    except ValueError: # dışardan bir değer hatası alındı
        print("dışardan bir değer hatası alındı")
        yield # -> eğer kullanmasaydık fonksiyonda başka bir yield yok dolayısıyla generator tükenirdi ve
        # hatadan sonra birde StopIteration hatası alınırdı

gen = coroutine()
next(gen) #  burda amacımız fonksiyonu ilerletmek idi çünkü hatanın yield satırında gönderirmesi gerek

gen.throw(ValueError)
gen.close()

# başka bir kullanım;

def coroutine():
    try:
        while True:
            yield "demir"
    except ValueError as a: # burda takma isim kullandık eğer amacın,istisna mesajını kullanmaksa burda as ifadesini kullanman gereklidir
        print("dışardan bir değer hatası alındı 2",a)
        yield # -> eğer kullanmasaydık fonksiyonda başka bir yield yok dolayısıyla generator tükenirdi ve
        # hatadan sonra birde StopIteration hatası alınırdı

gen = coroutine()
next(gen)

gen.throw(ValueError("Value Error YAKALANDI")) # bu yöntem modern halidir
# eskiden -> gen.throw(ValueError,ValueEror("Value Error YAKALANDI")) şeklinde yazılırdı ama bu yöntem eskidi eğer
# bunu kullanırsan uyarı sinyali alırsın