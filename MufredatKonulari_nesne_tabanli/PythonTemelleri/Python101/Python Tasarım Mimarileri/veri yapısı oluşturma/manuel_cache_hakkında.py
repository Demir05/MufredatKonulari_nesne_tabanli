# 🔍 NEDEN `str()` KULLANARAK CACHE ANAHTARI ÜRETMEK GÜVENLİ DEĞİLDİR?
from functools import lru_cache


# Python'da str(obj) çağrısı, objenin metinsel temsiline ulaşmak için kullanılır.
# Ancak objenin __str__() metodu tanımlı değilse veya default kalmışsa,
# çıktı genellikle objenin bellek adresini içerir:
# Örn: "<__main__.MyClass object at 0x10b2bfa90>"
# Bu çıktı, her nesne örneği için farklıdır — içeriği aynı olsa bile!

# Bu yüzden:
# Aynı içerikli iki nesne için bile `str()` farklı string döndürür
# ➤ Bu da `hash(str(obj))` gibi kullanımlarda hatalı cache anahtarı üretir.
# ➤ Cache sistemi, aynı içerik için tekrar tekrar hesaplama yapar (kötü!)

# ✅ ÇÖZÜM: BELLEK-BAĞIMSIZ, İÇERİK-TABANLI TEMSİLLER KULLANMAK

# Bunun için `stable_repr()` gibi bir fonksiyon tanımlarız:
# - dict nesneleri için: sorted(dict.items())
# - list/tuple nesneleri için: içeriklerini sabit sırada işlemek
# - objelerin __dict__ özelliğini kullanmak (varsa)
# Bu sayede, objenin içeriği aynıysa → aynı temsil, aynı hash!


def stable_repr(x):
    """
    stable_repr: Kararlı (deterministic) ve hashlenebilir temsil üretir.

    🔍 AMAÇ:
    ------------------------
    Bazı objeler (örneğin: list, dict, sınıf örnekleri) doğrudan hashlenemez.
    Bu fonksiyon, bu objeleri güvenli ve sabit (kararlı) şekilde temsil edecek
    bir yapı üretir. Bu sayede cache sistemleri (LRU gibi) güvenilir şekilde çalışır.

    ⚠️ Neden hash doğrudan çalışmaz?
        - list, dict gibi yapılar hashlenemez (mutable oldukları için)
        - objelerin id’si farklı olabilir, ama içerik aynı → hash anlamını yitirir

    📦 Nasıl çalışır?
    ------------------------
    - Eğer objenin __dict__’i varsa:
        Bu bir sınıf örneğidir → attribute’ları alınır ve sıralanmış tuple yapılır
    - Eğer objede __slots__ varsa:
        Sınıf sabit slotlarla tanımlanmıştır → slot içerikleri alınır
    - Eğer objemiz list/tuple ise:
        İçindeki elemanlar rekürsif olarak aynı şekilde işlenir
    - Eğer objemiz dict ise:
        key-value çiftleri sıralı olarak tuple’a çevrilir
    - Diğer tipler:
        str, int, bool gibi doğrudan hashlenebilen değerler direkt döner

    🔁 Bu sayede:
        Aynı içeriğe sahip yapılar aynı temsil ile hashlenir.
    """

    if hasattr(x, '__dict__'):
        # x bir sınıf örneği → attribute'ları __dict__ içinde
        # İçeriği sıralayıp tuple'a çevirerek hashlenebilir hale getiriyoruz
        return tuple(sorted(x.__dict__.items()))

    elif hasattr(x, '__slots__'):
        # Eğer sınıf __slots__ ile tanımlandıysa __dict__ olmayabilir
        # Slot'lardaki değerleri toplayarak kararlı temsili oluştur
        try:
            return tuple((slot, getattr(x, slot)) for slot in x.__slots__)
        except Exception:
            return str(x)  # Erişilemezse, string temsilini döner fallback

    elif isinstance(x, (list, tuple)):
        # Listeler ve demetler hashlenemez
        # İçeriklerini rekürsif olarak kararlı tuple temsile çevir
        return tuple(stable_repr(i) for i in x)

    elif isinstance(x, dict):
        # Sözlüklerde sıralama garantisi yok
        # Key-value çiftlerini sıralayıp tuple yap
        return tuple(sorted((k, stable_repr(v)) for k, v in x.items()))

    return x  # Eğer yukarıdakilere uymuyorsa, doğrudan döndür