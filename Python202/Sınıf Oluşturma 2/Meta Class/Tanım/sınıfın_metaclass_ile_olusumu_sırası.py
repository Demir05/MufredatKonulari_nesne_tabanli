class MetaInit(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        # 1️⃣ İlk adım: Sınıf gövdesi yazılmadan önce çağrılır
        # Bu metod, sınıf içinde tanımlanacak attribute'ların yazılacağı namespace'i belirler
        print("[__prepare__] çağrıldı")
        return dict()

    def __new__(cls, name, bases, namespace):
        # 2️⃣ İkinci adım: Sınıf gövdesi yazıldıktan sonra __new__ ile sınıf nesnesi oluşturulur
        print("[__new__] çağrıldı")
        print("  Namespace:", namespace)  # {'role': None, 'name': 'Ali'}
        return super().__new__(cls, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        # 3️⃣ Üçüncü adım: Sınıf bellekte oluşturulduktan sonra __init__ çağrılır
        # Artık sınıf objesi 'cls' tamamen erişilebilir, attribute'lara erişilebilir
        print("[__init__] çağrıldı")
        print("  cls.name:", cls.name)
        print("  cls.role:", cls.role)
        if cls.role is None:
            cls.role = "guest"


# 🔧 Bu sınıf tanımlandığında yukarıdaki akış çalışır:
class User(metaclass=MetaInit):
    role = None
    name = "Ali"

# ✅ Artık sınıf oluşturulmuştur:
print(User.role)  # guest
print(User.name)  # Ali
