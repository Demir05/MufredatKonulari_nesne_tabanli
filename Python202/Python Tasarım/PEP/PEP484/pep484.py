# 📘 PEP 484 – Type Hints
# Python'da statik tip ipuçları (type hints) eklemek için önerilen standarttır.
# Python 3.5 ile birlikte tanıtılmıştır.
# Amaç: Kodun ne tür veriyle çalıştığını açıkça belirtmek, analiz ve refaktör kolaylığı sağlamak.

# 🧠 Type Hint nedir?
# Fonksiyonların parametre ve dönüş tiplerini belirtmek için kullanılan bir sözdizimidir.
# Kodun davranışını değiştirmez, sadece IDE'ler ve analiz araçları için bilgi sağlar.


# ✅ Basit örnek
def selamla(isim: str) -> str:
    return f"Merhaba, {isim}"


# ❗ Not: Type hint'ler runtime'da kontrol edilmez.
# Ancak __annotations__ üzerinden erişilebilir:
print(selamla.__annotations__)  # {'isim': <class 'str'>, 'return': <class 'str'>}

# 📦 typing modülü: PEP 484 ile birlikte gelen yardımcı tipler içerir.
from typing import List, Dict, Tuple, Optional, Union, Any, Callable


# ✅ List, Dict, Tuple gibi koleksiyonlar için tip belirtimi
def ortalamalar(veriler: List[float]) -> float:
    return sum(veriler) / len(veriler)


def ayarlar() -> Dict[str, str]:
    return {"tema": "koyu", "dil": "tr"}


# ✅ Optional: None dönebilecek tipler için
def bul(id: int) -> Optional[str]:
    return None if id == 0 else str(id)


# ✅ Union: Birden fazla olası tip için
def çöz(değer: Union[int, str]) -> str:
    return str(değer)


# ✅ Any: Her tür veri kabul edilir
def işleme(veri: Any) -> None:
    print(veri)


# ✅ Callable: Fonksiyon parametresi tanımlamak için
def çalıştır(f: Callable[[int], str], x: int) -> str:
    return f(x)


# ✅ Tuple: Sabit uzunlukta diziler için
def koordinat() -> Tuple[float, float]:
    return (41.0, 29.0)


# ✅ Nested yapı örneği
def yapılandırma() -> Dict[str, Union[str, List[int]]]:
    return {"mod": "aktif", "portlar": [80, 443]}


# 🧩 Gradual Typing (Kademeli Tip Belirtimi)
# PEP 484, tüm kodun tiplenmesini zorunlu kılmaz.
# İstersen sadece bazı fonksiyonlara tip ekleyebilirsin.
# Bu esneklik sayesinde eski kodlarla uyum korunur.

# 🧪 Statik analiz araçları
# Type hint'ler sayesinde mypy, pyright gibi araçlar kodu analiz edebilir.
# Hatalar daha yazım aşamasında yakalanabilir.

# 🎯 Senin gibi mimari düşünen biri için ne ifade eder?
# - Kodun veri akışı netleşir
# - Edge-case'ler daha erken yakalanır
# - Refaktör ve test süreçleri kolaylaşır
# - safe_repr gibi fonksiyonlarda davranış daha açık hale gelir


# ✅ Örnek: safe_repr için type hint
def safe_repr(obj: Any, seen: Optional[set] = None, depth: int = 0) -> str: ...


# 🔚 Sonuç:
# PEP 484, Python'un dinamik doğasını korurken, büyük projelerde tip güvenliği ve sürdürülebilirlik sağlar.
# Kodun ne beklediği ve ne döndürdüğü açıkça yazıldığında, mimari hatalar azalır.
