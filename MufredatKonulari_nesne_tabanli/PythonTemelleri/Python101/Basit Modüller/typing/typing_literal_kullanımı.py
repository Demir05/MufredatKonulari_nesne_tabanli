# 🧾 Literal — Tip Belirleyici Sabitler (typing.Literal)
# -----------------------------------------

# 🔹 Literal, bir değerin *sadece belirli sabitlerden biri* olabileceğini belirtmek için kullanılır.
# 🔹 Bu, hem tip kontrol araçlarına (mypy, pyright), hem de IDE'lere bilgi verir.
# 🔹 Python 3.8+ ile kullanılabilir (daha eski sürümlerde typing_extensions üzerinden alınır)

from typing import Literal

# 🎯 Örnek: Bir fonksiyon sadece 3 farklı string alabilsin
def set_status(status: Literal["draft", "published", "archived"]) -> None:
    print(f"Durum: {status}")

set_status("published")  # ✅ geçerli
set_status("deleted")    # ❌ mypy/pyright uyarı verir — "deleted" izin verilen bir değer değil

# ✅ Faydaları:
# ----------------------
# 1. Kod güvenliğini artırır (yanlış değer girildiğinde uyarı verir)
# 2. Otomatik tamamlama (IDE'lerde `mode=` yazınca değerleri önerir)
# 3. Daha iyi dokümantasyon sağlar (ne beklediğini tipten anlayabilirsin)
# 4. Hata ayıklamayı kolaylaştırır

# 🔒 Not:
# Literal değerler sabittir — dinamik string'ler (örneğin input) buna uymayabilir

# 🛠️ Class İçinde Kullanımı

class InjectOperators:
    def __init__(
        self,
        target: str,
        mode: Literal["left", "inplace", "right"],  # ✅ sadece bu 3 değerden biri olmalı
        ops: tuple = (),
        *class_args
    ):
        self.target = target
        self.mode = mode
        self.ops = ops
        self.class_args = class_args
