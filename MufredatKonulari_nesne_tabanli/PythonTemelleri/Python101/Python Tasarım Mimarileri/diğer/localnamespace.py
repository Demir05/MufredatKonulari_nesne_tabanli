# 📘 Bu dosyada Python'da dinamik isim oluşturma, yerel kapsam yönetimi
# ve `exec()`/`eval()` fonksiyonlarının nasıl güvenli ve kontrol edilebilir şekilde
# kullanılabileceği örneklenmiştir.

# 🔹 1. DynamicNamespace: Dinamik isim alanı oluşturmak için basit bir sınıf.
# Bu sınıfa istediğimiz kadar dinamik attribute ekleyebiliriz.

class DynamicNamespace:
    """
    🔧 Dinamik olarak attribute eklenebilen, sınırlı bir isim alanı (namespace).
    Bu yapı, global scope'u kirletmeden değişken yönetimi sağlar.
    """
    def __init__(self):
        pass

    def __repr__(self):
        return f"<Namespace: {self.__dict__}>"


# 🔹 2. exec() kullanımı: Kodun dışarı sızmaması için özel bir local scope oluşturuyoruz.
# Bu sayede çalıştırdığımız kod sadece verdiğimiz local_scope üzerinde etkili olur.

kod = """
x = 10
y = 20
z = x + y
"""

# Local scope dictionary'si (boş)
local_scope = {}

# 🧪 exec() burada çok satırlı Python kodunu çalıştırır.
# globals: {} → dış dünya yok
# locals: local_scope → sadece bu sözlüğe etki edecek
exec(kod, {}, local_scope)

# 📥 exec() sonrası oluşan değişkenler `local_scope` içinde tutulur.
# Bunları kendi namespace objemize taşıyarak güvenli şekilde kullanabiliriz.

ns = DynamicNamespace()

# 🔁 local_scope'daki her değişkeni setattr ile DynamicNamespace objemize ekliyoruz.
for k, v in local_scope.items():
    setattr(ns, k, v)

# 🔍 Test:
# ns artık local_scope içeriğini taşır
print(ns)     # <Namespace: {'x': 10, 'y': 20, 'z': 30}>
print(ns.z)   # 30

# 💡 Neden Böyle Bir Yapı Kullanılır?
# - exec() ile oluşturulan değişkenler global scope'a bulaşmaz
# - Dinamik olarak değişken adları belirlenebilir
# - Güvenli, kontrollü, okunaklı bir kod ortamı sağlar
# - Scripting, DSL, analiz motorları gibi sistemler için temel oluşturur

# 🔒 Güvenlik Notu:
# - eval/exec kullanırken input'ları sanitize et
# - Kullanıcıdan gelen kod asla doğrudan çalıştırılmamalı
# - Basit işlemler için ast.literal_eval gibi güvenli fonksiyonlar tercih edilmeli
