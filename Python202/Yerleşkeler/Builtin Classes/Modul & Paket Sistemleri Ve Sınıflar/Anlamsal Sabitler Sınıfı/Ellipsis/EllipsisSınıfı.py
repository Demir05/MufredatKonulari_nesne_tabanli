# -*- coding: utf-8 -*-
# =============================================================================
#  PYTHON: Ellipsis — Sözel/Terorik Açıklama + Kullanım Alanları + Örnekler
# =============================================================================
#  "Ellipsis" Nedir?
# =============================================================================
# • Ellipsis, Python'da özel bir sabittir.
# • Yazım şekli:
#       Tam adı: Ellipsis
#       Kısa yazımı: ...
# • Türü: ellipsis
#       type(Ellipsis)  # <class 'ellipsis'>
#       Ellipsis is ... # True
# • Python çekirdeğinde çok fazla kullanılmaz ama bazı kütüphanelerde
#   ve tip ipuçlarında önemli rolleri vardır.
# =============================================================================


# =============================================================================
# 1) Kullanım Alanları
# =============================================================================
# 1.1 Yer tutucu (placeholder) olarak:
#     - Henüz yazmadığın bir fonksiyon, metod veya kod bloğu için geçici olarak
#       koyabilirsin. Bu sayede kod sentaks hatası vermez.
#     - "pass" ile benzer ama genellikle "buraya içerik gelecek" vurgusu için tercih edilir.
#
#     Örn:
#       def future_feature():
#           ...
#
# 1.2 Tip ipuçlarında (typing) kullanımı:
#     - "..." tip ipuçlarında anlam olarak "parametreleri önemseme" veya
#       "sonsuz uzunluk" gibi durumları belirtir.
#
#       Örn:
#         from typing import Callable
#         FuncType = Callable[..., int]     # Parametre sayısı ve türleri önemli değil, int döner
#
#         Numbers = tuple[int, ...]         # Sonsuz sayıda int alabilen tuple
#
# 1.3 Çok boyutlu dizilerde dilimleme (NumPy vb.):
#     - "..." eksik boyutları otomatik doldurur.
#
#       Örn:
#         import numpy as np
#         arr = np.arange(2*3*4).reshape(2,3,4)
#         arr[1, ...]   # arr[1, :, :] ile aynı
#         arr[..., 2]   # arr[:, :, 2] ile aynı
#
# 1.4 Pattern matching veya özel API'lerde sinyal değeri:
#     - Bazı kütüphaneler Ellipsis'i özel bir anahtar/sinyal olarak kullanır.
# =============================================================================


# =============================================================================
# 2) Özellikler
# =============================================================================
# • Tekil nesne: Ellipsis global olarak tek örnektir.
# • Doğruluk değeri: bool(Ellipsis) → True
# • Karşılaştırma: 'is' ile yapılır.
# =============================================================================


# =============================================================================
# 3) Örnekler
# =============================================================================

if __name__ == "__main__":
    # Tür kontrolü
    print(type(Ellipsis))   # <class 'ellipsis'>
    print(Ellipsis is ...)  # True

    # 1.1 Yer tutucu
    def placeholder():
        ...
    placeholder()  # Çalışır, hiçbir şey yapmaz

    # 1.2 Tip ipucu örneği
    from typing import Callable
    func_type: Callable[..., int]  # Parametre türleri önemli değil, int döner

    # 1.3 NumPy örneği
    import numpy as np
    arr = np.arange(2*3*4).reshape(2,3,4)
    print(arr[1, ...].shape)  # (3, 4)
    print(arr[..., 2].shape)  # (2, 3)

    # 2) Doğruluk değeri
    if Ellipsis:
        print("Ellipsis True kabul edilir")

    # Karşılaştırma
    if ... is Ellipsis:
        print("Ellipsis tekil nesnedir ✔️")
