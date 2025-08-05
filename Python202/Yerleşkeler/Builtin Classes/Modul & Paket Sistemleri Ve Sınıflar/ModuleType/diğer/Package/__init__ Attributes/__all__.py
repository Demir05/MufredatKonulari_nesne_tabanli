# ----------------- 🧪 Python'da __all__ Ne İşe Yarar? ------------------------

# ----------------------------------------------------------------------
# 📌 1. __all__ Nedir?
# ----------------------------------------------------------------------
# __all__, bir modül veya paketin içinden:
#   from <modül> import *
# ifadesiyle hangi sembollerin (değişken, sınıf, fonksiyon...) dışa aktarılacağını
# belirleyen özel bir liste değişkenidir.

# Bu liste string içerir ve import * sırasında sadece o listedeki isimler alınır.

# ----------------------------------------------------------------------
# 📌 2. Varsayılan Davranış (eğer __all__ yoksa)
# ----------------------------------------------------------------------
# Eğer __all__ tanımlı DEĞİLSE:
# - Python, modül içindeki tüm isimleri globals() ile alır
# - Ama sadece 'public' olanları dışa aktarır:
#     - Yani '_' ile başlamayanlar
#     - '__dunder__' isimleri alınmaz

# Bu, import * kullanımının bilinçli sınırlandırılmasıdır.

# Örnek:
# modül.py
# __version__ = "1.0.0"
# def foo(): pass
# def _bar(): pass

# from modül import *     → sadece foo gelir


# ----------------------------------------------------------------------
# 📌 3. __all__ Tanımlıysa Ne Olur?
# ----------------------------------------------------------------------
# Eğer __all__ listesi tanımlanmışsa:
# - import * sırasında SADECE bu listedeki isimler dışa açılır
# - Diğer hiçbir isim import edilmez, dunder bile olsa dahil edilmez
# - Yani __all__, export edilen API’yi kesin olarak belirler

# Örnek:
# __all__ = ['__version__', 'foo']

# from modül import *     → sadece __version__ ve foo alınır
# _bar veya başka hiçbir şey alınmaz


# ----------------------------------------------------------------------
# 📌 4. __all__ Sihirli Bir Yapı mıdır?
# ----------------------------------------------------------------------
# Hayır ❌
# __all__ bir descriptor değildir.
# __getattribute__, __dir__, __slots__ gibi özel davranış üretmez.
# Sadece import sistemine “liste şu” diye bilgi veren basit bir string listesidir.
# Yani dilin içsel motoruna değil, import davranışına yön verir.


# ----------------------------------------------------------------------
# 📌 5. Neden Dunder (örneğin __version__) isimleri alınmaz?
# ----------------------------------------------------------------------
# Çünkü dunder isimler:
# - Python yorumlayıcısına özel sistemsel üyedir (örneğin __loader__, __doc__, __file__)
# - import * ifadesiyle dışa çıkmaları risklidir
# - Namespace'i kirletmeleri, kullanıcıyı yanıltmaları olasıdır

# Bu nedenle:
# - Python yorumlayıcısı, import * sırasında dunder’ları otomatik olarak almaz
# - Ama sen istiyorsan __all__ listesine elle ekleyebilirsin

# Bu, dilin açık/kontrol edilebilir ve güvenli mimari yaklaşımının sonucudur.


# ----------------------------------------------------------------------
# 📌 6. Dinamik Olarak __all__ Üretilebilir mi?
# ----------------------------------------------------------------------
# Evet ✔️
# __all__ = [name for name in globals() if not name.startswith("_")]

# Ya da introspection ile:
# __all__ = [k for k, v in globals().items() if callable(v)]

# Bu, modül içeriğini dinamik olarak filtrelemeye yarar.


# ----------------------------------------------------------------------
# 📌 7. __all__ Nerede Kullanılmaz?
# ----------------------------------------------------------------------
# Sadece from <modül> import * sırasında etkilidir.
# Diğer tüm import biçimleri için __all__ göz önüne alınmaz.

# Örnek:
# from modül import foo    → __all__ kontrol edilmez
# import modül             → __all__ hiç kullanılmaz


# ----------------------------------------------------------------------
# ✅ SONUÇ:
# ----------------------------------------------------------------------
# __all__:
# - import * davranışını kontrol eder
# - Hangi sembollerin dışa açık olduğunu belirler
# - Dunder semboller varsayılan olarak alınmaz
# - import mekanizması dışında bir etkisi yoktur
# - Tamamen geliştiricinin yönetimindedir

# Bu liste sayesinde:
# - API kontrolü yapılır
# - Namespace kirlenmesi engellenir
# - Modül daha sürdürülebilir hale gelir ✔️
