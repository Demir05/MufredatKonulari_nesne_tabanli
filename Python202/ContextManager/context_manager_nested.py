# -------------------------------------------------------------------
# NESTED WITH (İÇ İÇE WITH) KULLANIMI
# -------------------------------------------------------------------
# Tanım:
# Birden fazla context manager’ı aynı anda açıp yönetmek için kullanılır.
# Python, açılışları sırayla yapar (soldan sağa),
# ama kapanışları ters sırada yapar (sağdan sola).
#
# Yani:
# with A() as a, B() as b:
#   gövde
#
# Eşdeğer:
# with A() as a:
#     with B() as b:
#         gövde
#
# Akış:
# 1. A.__enter__() çağrılır → a
# 2. B.__enter__() çağrılır → b
# 3. gövde çalışır
# 4. çıkışta: önce B.__exit__(), sonra A.__exit__()
#
# Not:
# Eğer ikinci context manager (B) açılırken hata olursa,
# A.__exit__() yine çağrılır → yani açılan tüm kaynaklar
# güvenle kapanır. Bu sayede try/finally yazmaya gerek kalmaz.
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# GERÇEK HAYAT KULLANIM ALANLARI
# -------------------------------------------------------------------

# 1) Birden fazla dosya açmak
# Örn: iki dosyayı karşılaştırmak
# with open("file1.txt") as f1, open("file2.txt") as f2:
#     for l1, l2 in zip(f1, f2):
#         print(l1.strip(), "|", l2.strip())
#
# - Her iki dosya da açılır
# - İşlem bittiğinde dosyalar doğru sırayla kapanır
# - Hata olsa bile dosyalar kapanır

# 2) Veritabanı + Log dosyası yönetimi
# with open("app.log", "a") as logfile, db_connection() as conn:
#     logfile.write("Transaction başlatıldı\n")
#     conn.execute("INSERT INTO users VALUES ('Ahmet')")
#
# - Aynı anda hem log dosyası hem veritabanı bağlantısı yönetilir
# - Transaction hataya düşerse:
#   → conn rollback yapar
#   → logfile kapanır

# 3) Birden fazla lock elde etmek (çok iş parçacıklı programlama)
# import threading
# lock1 = threading.Lock()
# lock2 = threading.Lock()
#
# with lock1, lock2:
#     # Kritik bölüm
#     print("Her iki lock elde edildi")
# # Çıkışta lock1 ve lock2 serbest bırakılır

# 4) Network bağlantısı + timeout kontrolü
# with socket.create_connection(("example.com", 80)) as sock, timeout_manager(5):
#     sock.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
#     response = sock.recv(4096)
#
# - Aynı anda hem network bağlantısı hem de timeout yöneticisi açılır
# - Timeout olursa bağlantı güvenle kapanır

# 5) Geçici config değişikliği + işlem
# with temp_env("MODE", "TEST"), open("debug.log", "w") as log:
#     log.write("Test modunda işlem başladı\n")
#     run_tests()
#
# - Çevresel değişken geçici olarak ayarlanır
# - Log dosyası açılır
# - Çıkışta hem env eski haline döner hem dosya kapanır

# -------------------------------------------------------------------
# ÖZET:
# - Nested with, birden fazla kaynağı aynı anda yönetmek için idealdir.
# - Açılış: soldan sağa
# - Kapanış: sağdan sola
# - Hata olsa bile her context manager garantiyle kapanır.
# - En sık: dosya işlemleri, db bağlantıları, loglama, lock, network.
# -------------------------------------------------------------------

class A:
    def __enter__(self):
        print(' A.__enter__')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(' A.__exit__')
        return False


class B:
    def __enter__(self):
        print(' B.__enter__')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(' B.__exit__')
        return False


with A():
    print("A için with bloğu")
    with B():
        print("B için wtih bloğu")

"""
 A.__enter__
 
A için with bloğu

 B.__enter__
 
B için wtih bloğu

 B.__exit__
 
 A.__exit__
"""

(insa := type.__dict__['__call__'].__get__(A, type).__call__()).__class__.__enter__(insa)  # A.__enter__
(insb := type.__dict__['__call__'].__get__(B, type).__call__()).__class__.__enter__(insb)  # B.__enter__
insb.__class__.__exit__(insb, None, None, None)  # B.__exit__
insa.__class__.__exit__(insa, None, None, None)  # A.__exit__

with A(), B():
    print('b için with2')
