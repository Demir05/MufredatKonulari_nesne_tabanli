# ================================================================
# 🔍 TYPING: "..." NE ANLAMA GELİR? (Callable vs Tuple farkı)
# ================================================================

# 🎯 1. Callable[..., ReturnType]
# --------------------------------
# 📌 Anlamı: Her türde ve sayıda argüman kabul eden bir fonksiyon.
# ✅ Örnek:
#     from typing import Callable
#     f: Callable[..., int]
#
#     def örnek1(): return 42
#     def örnek2(a, b, c): return a + b + c
#
#     f = örnek1  ✅
#     f = örnek2  ✅
#
# ⚠️ Burada "..." → türü ÖNEMSEMEZ, sadece dönüş türü önemlidir.

# 🎯 2. Tuple[SomeType, ...]
# --------------------------------
# 📌 Anlamı: Her uzunlukta, ama sadece TEK TÜRDE öğelerden oluşan bir tuple.
# ✅ Örnek:
#     t1: Tuple[int, ...] = (1, 2, 3, 4)        ✅
#     t2: Tuple[str, ...] = ("a", "b", "c")     ✅
#     t3: Tuple[int, ...] = (1, "x", 3)         ❌  (str içeriyor!)

# ⚠️ Burada "..." → UZUNLUK esnek, ama TÜRLER sabit olmalı.

# ================================================================
# 🧠 AKILDA KALSIN:
# ------------------------------------------------
# Callable[..., T]  →  Parametre fark etmez, dönüş T
# Tuple[T, ...]     →  Her eleman T olmalı, sayısı fark etmez
# ================================================================

from typing import List

liste:List[str] = ["d","e","m"]





