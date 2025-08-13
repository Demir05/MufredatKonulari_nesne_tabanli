# -*- coding: utf-8 -*-
# =============================================================================
#  PYTHON: NoneType ve None — Sözel/Terorik Açıklama + Kullanım Alanları + Örnekler
# =============================================================================
#  Bu dosya tamamen "# yorum satırları" ile anlatım odaklıdır; en sonda kısa,
#  çalıştırılabilir örnekler bulunur.
#
#  İçerik Sırası:
#    1) NoneType — Sınıfın Doğası (teorik açıklama)
#    2) None — NoneType'ın Tek Örneği (teorik açıklama)
#    3) NoneType'daki dunder (özel) metotların davranışı (profesyonel düzeyde)
#    4) Doğru/yanlış kullanım kalıpları (tasarım notları)
#    5) Örnekler (çalıştırılabilir kısa demolar)
#
#  Notasyon:
#    - "Anlamsal sabit": Dilde özel anlamı olan tekil semboller (None gibi).
#    - "Singleton": Tek örnek. Python'da None, NoneType'ın singleton örneğidir.
# =============================================================================


# =============================================================================
# 1) NoneType — Sınıfın Doğası (Nedir, ne işe yarar, nerelerde kullanılır?)
# =============================================================================
# • NoneType, Python dilinde "değer yok / atanmadı / bilinmiyor" anlamına gelen
#   tekil nesne olan None'ın (singleton) ait olduğu sınıftır.
# • Standart Python kodunda NoneType'ı kendiniz örnekleyemezsiniz (constructor
#   dışa kapalıdır); NoneType() çağrısı çalışır ama yine None nesnesi döner.
# • NoneType, miras almak için tasarlanmamıştır; alt sınıf oluşturmaya çalışmak
#   da TypeError ile sonuçlanır.

# • Tasarım amacı:
#     - Dilde "değer yok" durumunu tek ve sabit bir sembolle temsil etmek,
#     - Programcılara basit ve performanslı bir kimlik karşılaştırması (is)
#       imkânı sağlamak,
#     - API'lerde isteğe bağlı argüman/sentinel örüntüsünü standardize etmek.

# • Nerelerde kullanılır?
#     - Fonksiyonların "dönüş değeri yok" durumu (return yazılmazsa None döner)
#     - Varsayılan parametre değeri (None = "hiç verilmedi" sinyali olarak)
#     - Veri yapılarında "bilinmiyor/eksik" işaretçisi (ancak domain anlamı
#       açısından bazen özel sentinel veya ayrı bir tür daha doğrudur)


# =============================================================================
# 2) None — NoneType'ın Tek (Singleton) Örneği
# =============================================================================
# • None, NoneType sınıfının tek örneğidir. Yorumlayıcı başlarken yaratılır ve
#   tüm program boyunca aynıdır.

# • "Singleton neden?" — Dilin anlamsal tutarlılığı: "değer yok" kavramı tek bir
#   sabit ile ifade edilir. Bu sayede 'is' ile kimlik karşılaştırması güvenilirdir.

# • Çoğaltılamaz: copy.copy(None) ve copy.deepcopy(None) yine None döndürür;
#   bu, immutability ve tekillik prensibinin bir sonucudur.

# • None'un doğruluk değeri (truthiness) False'tur; koşullarda "yok/boş"
#   davranışı beklenir (if None: bloğu çalışmaz).

# • None değiştirilemez (immutable); herhangi bir öznitelik ataması yapılamaz.

# • None adı dil seviyesinde sabittir; yeniden bağlamak (None = 5) SÖZDİZİMSEL
#   olarak yasaktır (SyntaxError).


# =============================================================================
# 3) NoneType İçindeki Dunder (Özel) Metotların Davranışı — Profesyonel Düzey
# =============================================================================
# 3.1 __repr__(self) → str
#     - Temsili string "None" olarak döner.
#     - Konsolda/LOG'larda görülen çıktı: >>> None  -> None
#
# 3.2 __bool__(self) → bool
#     - None, bool bağlamında False döner.
#       Örn: bool(None) == False.
#
# 3.3 __hash__(self) → int  (object'ten gelir)
#     - None hash'lenebilir (dict/set anahtarı olarak kullanılabilir).
#     - Hash değeri uygulama detaydır; belirli bir sabit olmasına güvenmeyin.
#       (CPython'da süreç içinde tutarlı, ancak sürüm/uygulama bağımlıdır.)
#
# 3.4 __eq__(self, other) ve __ne__(self, other)  (object semantiği)
#     - NoneType özel bir eşitlik mantığı eklemez; object düzeyinde kimlik
#       temelli eşitlik geçerlidir. "None == None" True, "None == X" (X ≠ None) False.
#     - Python stili gereği None ile karşılaştırmalarda '==' yerine 'is' kullanılır.
#       Gerekçe: '==' operatör aşırı yüklenebilir (üçüncü parti tipler sürpriz yapabilir),
#       'is' ise kimlik kontrolüyle dilin garantilediği davranışı verir.
#
# 3.5 Karşılaştırmalar (__lt__, __le__, __gt__, __ge__)
#     - None ile sıralama ilişkili karşılaştırmalar (örn. None < 1) Python 3'te
#       TypeError yükseltir. (Python 2'de bazı "top-level" karşılaştırmalar
#       vardı; artık yok.)
#
# 3.6 Örneklenemezlik / Kurucu engeli (__new__/__init__)
#     - NoneType'ın örnek üretimi C düzeyinde engellenir; kullanıcı kodundan
#       NoneType() çağrılamaz. Alt sınıf oluşturmak da yasaktır (TypeError).
#
# 3.7 Öznitelik yönetimi (__setattr__, __delattr__)
#     - None üzerinde öznitelik ataması/silmesi desteklenmez (AttributeError).
#
# 3.8 MRO (Method Resolution Order)
#     - type(None).__mro__ => (NoneType, object)
#     - Davranışların çoğu object'ten miras alınır; yalın ve minimal bir tiptir.


# =============================================================================
# 4) Tasarım / Kullanım Kalıpları — Doğru ve Yanlış Yaklaşımlar
# =============================================================================
# ✅ DOĞRU: Kimlik kontrolüyle test
#   if x is None: ...
#   if x is not None: ...
#
# ✅ DOĞRU: None'ı "atanmadı" anlamında sentinel olarak kullanmak
#   def f(path=None):
#       if path is None:
#           path = "default.json"
#
# ✅ DOĞRU: None'ın bool değeri üzerinden koşul (niyet açıksa)
#   if result is None:
#       handle_missing()
#
# ⚠️ DİKKAT: '==' yerine 'is' kullanın
#   if x == None:  # anti-pattern: operatör aşırı yüklemeleri tuzak olabilir
#       ...
#
# ⚠️ DİKKAT: "None geçerli bir değer mi?" belirsizliğinde özel sentinel
#   _sentinel = object()
#   def f(x=_sentinel):
#       if x is _sentinel:  # argüman hiç verilmedi
#           ...
#       else:
#           ...             # x None olabilir ve bu geçerli bir değer olabilir
#
# ⚠️ DİKKAT: None ile sıralama karşılaştırmaları (</>) geçersizdir (TypeError).
#
# ⚠️ DİKKAT: None'ı sayısal işlemlerde "0" gibi muamele etmek hatalıdır.
#   count = count or 0
#   # Bu kalıp, "0" ile "None"ı aynı kefeye koyar; bazı durumlarda istenmez.
#
# Tasarım İlkesi:
#   - None "değer yok" demektir; veri modelinizde "bilinmiyor" ile "boş"
#     ayrışıyorsa, ayrı tür/sentinel kullanın.
#   - API yüzeylerinde "None = varsayılan" desenini net dökümante edin.


# =============================================================================
# 5) ÖRNEKLER — Kısa, Çalıştırılabilir Demolar
# =============================================================================

if __name__ == "__main__":
    # --- Tür ve tekillik ---
    assert type(None).__name__ == "NoneType"
    import types
    # Python 3.10+: types.NoneType erişilebilir
    try:
        assert types.NoneType is type(None)
    except AttributeError:
        # Daha eski bir sürümde olabilir; sorun değil.
        pass

    # Tekil kimlik garantisi
    a = None
    b = None
    assert a is b

    # Doğruluk değeri
    assert bool(None) is False

    # Hash'lenebilirlik (uygulama detayına güvenmeden sadece "hashlenebilir" olması)
    s = {None}
    assert None in s

    # Karşılaştırma semantiği
    assert (None == None) is True          # eşitlik True
    assert (None != "x") is True           # None, "x" ile eşit değildir
    # Sıralama karşılaştırmaları TypeError: yorum satırını açarsanız hata alırsınız
    # _ = (None < 1)

    # Doğru kontrol: is / is not
    value = None
    if value is None:
        value = "defaulted"
    assert value == "defaulted"

    # Sentinel örüntüsü
    _sentinel = object()
    def load_config(path=_sentinel):
        if path is _sentinel:
            return "load default config"
        if path is None:
            return "explicitly requested: no path (None)"
        return f"load from {path}"

    assert load_config() == "load default config"
    assert load_config(None) == "explicitly requested: no path (None)"
    assert load_config("cfg.json") == "load from cfg.json"

    # Örneklenemezlik göstergesi (TypeError yakalama)
    import builtins
    try:
        # types.NoneType()  # 3.10+; TypeError
        # getattr ile yaklaşıp denemek yerine doğrudan söylem: örneklenemez.
        pass
    except TypeError:
        pass

    print("Tüm None/NoneType demoları başarıyla geçti. ✔️")
