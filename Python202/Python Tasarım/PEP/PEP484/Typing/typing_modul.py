# 🔹 Any
# Her tür veri kabul edilir. Tip kontrolü yapılmaz.
# Genellikle dış kaynaklardan gelen veri, JSON, config, dinamik içerikler için kullanılır.
# Fazla kullanımı type safety'yi azaltır.Ayrıca PEP8'i de ihlal eder çünkü;
# fazla Any kullanımı demek kodda belirsizlik var demektir oysa ki Interpereter 'belki boyle çalışır'... çalışmaz
# kod,tahmin edilebilir,net ve açık olmalıdır bu nedenle çok sık Any kullanımından kaçın.

from typing import Any, Final


def serialize(data: Any) -> str:
    return str(data)


def log_event(event: Any) -> None:
    print(f"Event: {event}")


# 🔹 Optional[X]
# Belirtilen tipe ek olarak None da kabul edilir.
# Optional[X] ≡ Union[X, None]
# Genellikle opsiyonel parametreler, nullable dönüşler, default değerler için kullanılır.

from typing import Optional


def get_user(id: int) -> Optional[str]:
    if id == 0:
        return None
    return f"user_{id}"


def parse(text: Optional[str]) -> str:
    return text or "default"


# 🔹 Union[X, Y, ...]
# Birden fazla olası tip belirtmek için kullanılır.
# Genellikle overload yerine tercih edilir.
# Python 3.10+ ile X | Y şeklinde yazılabilir.

from typing import Union


def stringify(value: Union[int, float]) -> str:
    return str(value)


def normalize(data: Union[str, List[str]]) -> List[str]:
    return data.split() if isinstance(data, str) else data


# 🔹 List[X], Dict[K, V], Tuple[X, Y], Set[X]
# Koleksiyon tipleri için kullanılır.
# Python 3.9+ ile yerleşik tipler doğrudan kullanılabilir: list[int], dict[str, str], vs.

from typing import List, Dict, Tuple, Set


def mean(values: List[float]) -> float:
    return sum(values) / len(values)


def config() -> Dict[str, Union[str, int]]:
    return {"mode": "dark", "timeout": 30}


def bounds() -> Tuple[int, int]:
    return (0, 100)


colors: Tuple[int, ...] = (
        1,
        2,
        3,
        4,
        5,
        6,
)  # sonsuz/belirsiz sayıda öğe belirtmek için Ellipsis kullanılır.

random: Tuple[int, str, float, bool] = (1, "demir", 1.4, True)


def tags() -> Set[str]:
    return {"python", "typing", "pep484"}


# 🔹 Callable[[ArgTypes], ReturnType]
# Fonksiyon veya çağrılabilir nesne tanımlamak için kullanılır.
# Genellikle callback, strateji pattern, dependency injection gibi yapılarda kullanılır.

from typing import Callable


def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)


def pipeline(steps: List[Callable[[str], str]], input: str) -> str:
    for step in steps:
        input = step(input)
    return input


# 🔹 TypeVar
# Generic fonksiyon ve sınıflar için parametrik tip tanımı sağlar.
# Genellikle veri yapıları, wrapper'lar, container'lar için kullanılır.

from typing import TypeVar, List

T = TypeVar("T")


def first(items: List[T]) -> T:
    return items[0]


def swap(a: T, b: T) -> Tuple[T, T]:
    return b, a


# 🔹 Generic
# Sınıflarda TypeVar ile birlikte kullanılır.
# Genellikle reusable container yapıları için tercih edilir.

from typing import Generic


class Box(Generic[T]):
    def __init__(self, content: T) -> None:
        self.content: T = content

    def get(self) -> T:
        return self.content


class Pair(Generic[T]):
    def __init__(self, left: T, right: T) -> None:
        self.left: T = left
        self.right: T = right


# 🔹 Kullanım örnekleri
kutu1 = Box  # T = int
kutu2 = Box[str]("merhaba")  # T = str

# kutu1.get() → int
# kutu2.get() → str

# 🔹 IDE ve analiz araçları bu tipleri tanır:
# - kutu1.get() çağrısı int döner
# - kutu2.get() çağrısı str döner
# - Oto tamamlama ve refaktör güvenliği sağlanır

# 🔹 Teknik olarak ne olur?
# Box[int] → Box.__class_getitem__(int) çağrısı tetiklenir
# typing.Generic sınıfı bu metodu override ettiği için hata alınmaz
# Eğer __class_getitem__ tanımlı olmasaydı:
# TypeError: 'type' object is not subscriptable

# 🔹 Mimari avantajlar
# - Kodun açıklanabilirliği artar
# - Sınıf davranışı dışarıdan gelen tipe göre şekillenir
# - Reusable ve sürdürülebilir yapı kurulur
# - Edge-case'lerde tip hatası önlenir

# 🔚 Sonuç:
# Generic[T] + TypeVar + __class_getitem__ → Python'da tip bazlı sınıf tasarımının temelidir.
# Senin gibi mimari düşünen biri için bu yapı, modül sınırlarını ve veri akışını netleştirmek için vazgeçilmezdir.

# 🔹 Literal
# Sabit değerleri sınırlamak için kullanılır.
# Genellikle config, enum benzeri sabitler için tercih edilir.
# Literal,yalnızca statik değerler alabilir yani değişken,sınıf,fonksiyon alamaz çünkü bunlar runtime boyunca değişebilirler.
# verilen değerlerin değiştirilemez olmaları garanti edilmelidir yani verilen nesne, 'Mutable' olmalıdır.
# ayrıca statik olarak verilen değerin,korunmalı olması gerek örneğin singleton neslerden NotImplemented ve Ellipsis verilemez sadece None geçerli
# NotImplemented ve Ellipsis,korunmalı olmadığı için Literal'de kullanılamaz

from typing import Literal


def status_check(status: Literal["ok", "fail", "pending"]) -> bool:
    return status == "ok"


def mode_switch(mode: Literal["light", "dark"]) -> str:
    return f"Mode set to {mode}"


# 🔹 Final değişken tanımı
# Bu değişken bir kez tanımlanır ve daha sonra değiştirilemez.
# Statik analiz araçları (mypy, pyright) yeniden atamaya izin vermez.

API_KEY: Final = "abc123"
API_KEY = "xyz456"  # ❌ mypy uyarısı: Final değişken yeniden atanamaz


# 🔹 Final sınıf tanımı
# Bu sınıf başka sınıflar tarafından miras alınamaz.
# Özellikle sabit davranışlı utility sınıflar için kullanılır.

@final
class SabitSınıf:
    def işlem(self):
        return "Bu sınıf genişletilemez"


class AltSınıf(SabitSınıf):  # ❌ mypy uyarısı: final sınıf extend edilemez
    pass


# 🔹 Final metod tanımı
# Bu metod alt sınıflarda override edilemez.
# Mimari olarak davranışın sabit kalmasını garanti eder.
# ama @staticmethod veya @classmethod ile kullanılırsa IDE, uyarı verebilir çünkü;
# zaten bu fonksiyonların override edilmesi beklenmez bu nedenle IDE,bu işlemin gereksiz olduğunu belirtir
# ayrıca final decorator'ü bağımsız fonksiyonlarda kullanılamaz çünkü bağımsız fonksiyonlar,zaten override edilemezler

class A:
    @final
    def işlem(self):
        return "Bu metod override edilemez"


class B(A):
    def işlem(self):  # ❌ mypy uyarısı: final metod override edilemez
        return "Değiştirildi"


# 🔹 Final + Literal birlikte kullanım
# Hem sabit değer hem değiştirilemezlik garantisi sağlanır.

from typing import Literal

RENK: Final[tuple[Literal[255], Literal[255], Literal[255]]] = (255, 255, 255)
RENK = (0, 0, 0)  # ❌ mypy uyarısı: Final değişken yeniden atanamaz

# 🔹 Annotated
# Tipin yanında ek açıklama veya metadata taşımak için kullanılır.
# bu metadata, herangi bir python nesnesi olabilir bu özellik parametre için;
# açıklama metni, koşul(filter amaçlı fonksiyon), taşıyabilceği ekstra veri demektir.
# ama IDE veya mypy gibi statik analiz araçları Annotated için kontrol yapamazlar manuel yapılması gerek.
from typing import Annotated


def age_check(age: Annotated[int, "must be positive"]) -> bool:
    return age > 0


def email_field(email: Annotated[str, "must contain @"]) -> str:
    return email


# 🔹 NoReturn
# Fonksiyon hiçbir şey döndürmez, normal akışa dönmez.
# Genellikle exception fırlatan veya sonsuz döngü içeren fonksiyonlar için kullanılır.
# bir fonksiyon hiçbir şey döndürmüyorsa bile çağrılıp değeri,referans olarak saklanırsa değişkenin değeri,None olur
# ama NoReturn'de fonksiyonun asla hiçbir koşulda herangi bir değer dönmeyeceğini bildirir bu durumda x = func() yapılamaz !
# ayrıca NoReturn, başka bir type hint ile kullanılmamalı çünkü return değeri belirtmek amacıyla kullanılmaz

from typing import NoReturn


def crash(msg: str) -> NoReturn:
    raise RuntimeError(msg)


def hang() -> NoReturn:
    while True:
        pass


# 🔹 ClassVar
# Sınıf düzeyinde değişken tanımlar, örnek (instance) düzeyinde değildir.
# Genellikle sabitler, konfigürasyonlar, sınıf genelinde paylaşılan değerler için kullanılır.
# Not: ClassVar aynı zamanda Fİnal ile aynı anlama gelir bu nedene ikisinin beraber kullanılması gereksiz ve geçersizdir
# yalnızca ClassVar kullanımı yeterlidir

from typing import ClassVar


class Settings:
    default_language: ClassVar[str] = "tr"
    max_users: ClassVar[int] = 100


# 🔹 NewType
# Runtime'da aynı kalan ama type checker için farklı görünen yeni tip tanımı sağlar.
# Genellikle domain-specific ID'ler, ayrıştırılmış primitive'ler için kullanılır.
# NewType ile oluşturulan bir tür,tp parametresine verilen türün alt üyesi falan değildir typing.NewType örneği
# ama bu örnek ile oluşturulan nesne,tp parametresine verilen türün ta kendisidir(alt sınıfı değildir) yani örneği
# işte bu nedenden dolayı NewType,sentinel olarak kullanılamaz çünkü örnekler, her ne kadar typing için farklı görünseler/yorumlansalar da
# runtime'da aynı kalırlar.

from typing import NewType

UserID = NewType("UserID", int)
SessionID = NewType("SessionID", str)


def get_user(id: UserID) -> str:
    return f"User {id}"


def validate_session(sid: SessionID) -> bool:
    return sid.startswith("sess_")


# 🔹 get_type_hints fonksiyonu:
# Bu fonksiyon, verilen objenin (fonksiyon, sınıf, modül) parametre ve dönüş tipi ipuçlarını döndürür.
# Varsayılan olarak sadece temel tipleri döndürür. Annotated gibi ek bilgileri almak için include_extras=True gerekir.

# 🔹 include_extras=False → sadece temel tipleri döndürür
hints_basic = get_type_hints(foo)
print("# include_extras=False çıktısı:")
print(hints_basic)
# Çıktı: {'x': <class 'int'>, 'y': Literal['A', 'B'], 'z': <class 'int'>}
# → Annotated içeriği yok, sadece temel tipler var

# 🔹 include_extras=True → Annotated gibi metadata içeren tipleri de döndürür
hints_full = get_type_hints(foo, include_extras=True)
print("\n# include_extras=True çıktısı:")
print(hints_full)
# Çıktı: {'x': Annotated[int, 'pozitif', <function ...>], 'y': Literal['A', 'B'], 'z': <class 'int'>}
# → Annotated içeriği korunmuş şekilde döner


# 🔹 globalns
# get_type_hints içinde globalns, modül düzeyindeki isim çözümlemesi için kullanılır.
# Python burada gerçek bir dict bekler, çünkü get_type_hints, string tipleri çözmek için eval() fonksiyonunu kullanır.
# eval(expr, globalns, localns) şeklinde çalışır ve globalns parametresi olarak verilen yapı mutlaka dict olmalıdır.
# Eğer globalns olarak mappingproxy (örneğin Namespace.__dict__) verilirse, eval() bunu kabul etmez çünkü mappingproxy salt okunur ve dict API'sini tam sağlamaz.
# Bu nedenle çözümleme başarısız olur → NameError veya TypeError alınabilir.


# 🔹 localns
# localns, lokal bağlam için kullanılır: sınıf içi, fonksiyon içi, closure gibi durumlar.
# Burada mappingproxy gibi salt okunur yapılar da kabul edilir çünkü eval() değil, doğrudan isim eşleştirmesi yapılır.
# get_type_hints bu bağlamı daha esnek şekilde kullanır.


# Eğer ForwardRef çözümlemesi yapılmazsa NameError alınabilir:
# get_type_hints(foo)  # ❌ NameError: name 'UserId' is not defined

# Doğru çözümleme için globalns=globals() verilmelidir:
hints_with_globals = get_type_hints(foo, globalns=globals(), include_extras=True)
print("\n# globals ile ForwardRef çözümlemesi:")
print(hints_with_globals)
# Çıktı: 'z': <class 'int'> → çünkü 'UserId' = int olarak globals içinde tanımlı

# 🔹 get_origin ve get_args ile Annotated içeriğini parçalayabiliriz:
annotated_type = hints_with_globals["x"]
if get_origin(annotated_type) is Annotated:
    base_type, *metadata = get_args(annotated_type)
    print("\n# Annotated içeriği:")
    print("Temel tip:", base_type)  # int
    print("Metadata:", metadata)  # ['pozitif', <function ...>]


# 🔹 get_type_hints(modül)
# Eğer get_type_hints'e bir modül nesnesi verirsen, modül içindeki global değişkenlerin ve fonksiyonların
# tip ipuçlarını çözümlemeye çalışır.
# Ancak bu çözümleme sadece doğrudan modül düzeyinde tanımlanmış değişkenler için geçerlidir.
# Fonksiyonlar, sınıflar veya iç içe tanımlar için ayrı ayrı get_type_hints çağrısı gerekir.
# Ayrıca modülün __annotations__ özelliği varsa, get_type_hints bunu kullanarak çözümleme yapar.


def set_parent(p: "Person") -> None:
    pass


class Person: ...


# 🔹 get_origin
# Karmaşık tiplerin temel (orijinal) tipini döndürür.
# Örneğin Annotated[int, ...] gibi bir yapı varsa, get_origin bu yapının Annotated olduğunu söyler.
# Bu, tipin ne tür bir yapı olduğunu anlamak için kullanılır.
# Genellikle Annotated, Union, List, Tuple gibi bileşik tiplerde kullanılır.
# Eğer verilen tip basit bir tipse (örneğin int, str), get_origin None döner.

# 🔹 get_args
# Karmaşık tiplerin içindeki bileşenleri (alt tipleri veya metadata) tuple olarak döndürür.
# Annotated[int, "meta", lambda x: x > 0] gibi bir yapı varsa, get_args bu yapıyı (int, "meta", <function>) şeklinde parçalar.
# Union[int, str] → (int, str)
# List[str] → (str,)
# Annotated → (temel tip, açıklama, metadata...)

# Bu iki fonksiyon birlikte kullanıldığında, tipin hem yapısını hem içeriğini introspect etmek mümkün olur.

# 🔹 Self (Python 3.11+)
# Metotlarda kendini tip olarak belirtmek için kullanılır.
# Genellikle fluent API, chaining pattern, builder yapılarında tercih edilir.

# from typing import Self

# class Chain:
#     def add(self, value: int) -> Self:
#         ...
#         return self

# 🔹 assert_type (Python 3.12+)
# Test amaçlı tip doğrulama sağlar.
# Genellikle unit testlerde veya IDE destekli tip kontrolünde kullanılır.
# bazen IDE ve mypy, karışık tiplerde yanlış tahminde bulunabilir assert_type, nokta atışı olarak kontrol sağlar
# ama assert_type'in Runtime'da hiçbir etkisi yoktur çalışmaz. sadece statik analiz araçları bunu dikkate alır.
# ayrıca büyük projelerde kodun niyetini daha açık belirtmek için kullanılabilir

# from typing import assert_type
# assert_type("hello", str)

# 🔹 ForwardRef
# Python'da bir fonksiyon veya sınıf tanımı içinde henüz tanımlanmamış bir türü referans göstermek gerektiğinde,
# bu tür string olarak yazılır: örneğin "User" gibi.
# Python bunu bir Forward Reference (ileri tür bildirimi) olarak yorumlar.
# Bu referanslar, runtime'da çözülmesi için get_type_hints gibi introspection araçlarında globalns/localns bağlamına ihtiyaç duyar.

# 🔹 Ama artık Python 3.7+ ile birlikte gelen `from __future__ import annotations` sayesinde,
# tüm tip ipuçları (type hints) otomatik olarak string olarak saklanır.
# Bu sayede ileri tür bildirimi yapmak için özel bir şey yapmaya gerek kalmaz.
# Yani artık "User" yerine doğrudan User yazabiliriz, çünkü çözümleme runtime'a ertelenmiştir.

# 🔹 Bu davranışın avantajı:
# - Modül içindeki türler sırasız tanımlanabilir
# - Recursive veri yapıları daha sade tanımlanabilir
# - Tip ipuçları daha hafif ve introspect edilebilir hale gelir


# 🔹 @overload (typing.overload)
# Bir fonksiyonun farklı parametre imzalarına göre farklı dönüş tiplerine sahip olduğunu
# statik tip denetleyicilere (mypy, pyright) bildiren dekoratördür.
# Runtime’da hiçbir etkisi yoktur; gövdesi çalıştırılmaz (… veya pass kullanılır).
# Tüm @overload imzaları üstte gelir, gerçek implementasyon en altta tek bir def ile yazılır.
# Amaç: Union ile ifade edilemeyen “girdi → çıktı” eşlemesini kesinleştirmek (inputa göre dar dönüş tipi).

# 🔹 get_overloads (typing.get_overloads)
# Verilen gerçek implementasyon fonksiyonu için tanımlanmış @overload imzalarının bir listesini döndürür.
# Bu, runtime’da overload imzalarına introspection yapabilmek içindir (sadece tip imzası verisi; mantık yok).
# Tipik kullanım: dekoratörler, dokümantasyon üreticileri veya imza tabanlı validasyon sistemlerinde.

# 🔹 clear_overloads (typing.clear_overloads)
# Verilen gerçek implementasyonla ilişkilendirilmiş @overload imzalarını temizler.
# Özellikle modül yeniden yükleme (hot-reload), dinamik tanım/yeniden tanım senaryolarında tutarlılık için kullanılır.
# overload,runtime'da çalışmaz ama iz bırakır bu izleri silmek reload işlemlerinde ve bellek tasarrufu için kritik olabilir.
# ───────────────────────────────────────────────────────────────────────────────

# 🔹 Overload çözümleme kuralları (statik analiz mantığı)
# - @overload imzaları sıralıdır: Tip denetleyici en üstten alta doğru en uyumlu imzayı seçer.
# - İmzalar birbiriyle çakışmayacak şekilde tasarlanmalıdır (aksi halde uyarı verebilir).
# - Implementasyon fonksiyonunun imzası, tüm @overload imzalarını kapsayacak şekilde genel olmalıdır.
# - @overload gövdeleri çalışmaz; sadece tip imzası taşır.

# 🔹 Union vs @overload
# - Union dönüş tipi, “her zaman bu birleşimden biri döner” der; inputa göre daraltılmış garanti vermez.
# - @overload ise “şu girdi gelirse dönüş tam olarak budur” diye net eşleşme bildirir (daha kesin sözleşme).

# 🔹 Literal ile değer-tabanlı overload
# - Literal[True]/Literal[False] gibi sabit değerlerle imza ayrıştırması yapılabilir.
# - Amaç: Parametrenin gerçek değerine göre tipin daralmasını statik olarak tanımlamak.

# 🔹 TypeVar ile jenerik overload
# - TypeVar, tek bir jenerik imza yerine birden fazla kesin imzayı @overload ile parçalamayı gereksiz kılabilir.
# - Ancak farklı giriş tiplerinin farklı dönüş tipleri (co/contra-variance veya shape) varsa @overload tercih edilir.

# 🔹 ParamSpec ve Concatenate ile callable overload
# - ParamSpec, bir çağrılabilirin parametre listesini taşır; Concatenate ile başa ek parametreler eklenebilir.
# - Decorator benzeri sarmalamalarda “girdi imzasını koru + ekstra parametre/çıktı değiş” senaryoları için idealdir.
# - @overload + ParamSpec birlikte, farklı çağrı şekillerini tip güvenli biçimde ifade etmenizi sağlar.

# 🔹 Metotlar ve sınıf bağlamında overload
# - @overload, instance method, classmethod ve staticmethod üzerinde de kullanılabilir.
# - Sıralama: tüm @overload’lar (gövdesiz) → en altta tek bir gerçek implementasyon (ilgili decorator ile).
# - self/cls parametreleri imzada yer alır; overload eşleşmesi bunları da dikkate alır (özellikle protokollerle).

# 🔹 Runtime davranışı ve sınırlamalar
# - @overload sadece tip sistemine sinyal taşır; Python runtime’da seçim yapmaz.
# - Gerçek davranışı implementasyon fonksiyonu belirler; isinstance/if/elif ile ayrım yapmanız gerekir.
# - get_overloads/clear_overloads introspection ve temizlik sağlar; “otomatik dispatch” sağlamazlar.

# 🔹 singledispatch ile farkı (functools.singledispatch)
# - singledispatch runtime’da tip tabanlı çok-biçimlilik sağlar (tek argümana göre).
# - @overload ise statik; type checker içindir. Çalışma anında dispatch yapmaz.
# - Birlikte kullanılabilir: @overload ile sözleşmeyi bildir, singledispatch ile gerçek dispatch’i uygula.

# 🔹 Hata örüntüleri ve iyi uygulamalar
# - Çakışan overload imzaları → tip denetleyiciden uyarı alırsınız; en spesifikten genele sıralayın.
# - Implementasyon imzası, tüm overload’ları kapsayacak kadar genel olmalı; aksi halde tip uyumsuzluğu doğar.
# - İmzaları kısa ve tek amaçlı tutun; Literal ve Union’u aşırı karmaşıklaştırmayın (bakım yükü artar).

# 🔹 IDE vs. denetleyici ve neden @overload?
# - IDE çoğu zaman sezgisel daraltma yapar, ancak garanti vermez.
# - @overload ile “girdi → çıktı” eşleşmesini resmi ve denetlenebilir şekilde belgeleyip doğrulatmış olursunuz.
# - Büyük kod tabanlarında dokümantasyon ve regresyon için overload imzaları güçlü bir sözleşmedir.

# 🔹 Overload Zinciri ve Bozulma Durumu

# @overload dekoratörleri, bir fonksiyonun farklı parametre imzalarına göre
# farklı dönüş tiplerine sahip olduğunu statik tip denetleyiciye bildiren yapılardır.
# Bu imzalar bir "zincir" oluşturur ve type checker (örneğin mypy) bu zinciri kesintisiz olarak yorumlar.

# ✅ Doğru kullanım:
# - Tüm @overload imzaları ardışık ve kesintisiz biçimde tanımlanmalıdır.
# - Zincirin sonunda tek bir gerçek implementasyon (def ile) yer almalıdır.
# - Araya hiçbir ifade (print, import, def, class, vs.) girmemelidir.

# ❌ Zincir bozulursa ne olur?
# - Eğer overload imzaları arasına başka bir ifade girerse, type checker zincirin bittiğini varsayar.
# - Bu durumda sonraki @overload imzaları yok sayılır.
# - Runtime’da hata alınmaz çünkü @overload zaten çalıştırılmaz.
# - Ancak statik analizde tip çıkarımı eksik veya hatalı olur → tip denetimi başarısız olabilir.

# 🔍 Örnek:
# @overload
# def func(x: int) -> int: ...
# print("Bu ifade zinciri böler")  # ❌ zincir bozuldu
# @overload
# def func(x: str) -> str: ...     # ❌ bu imza artık yok sayılır
# def func(x): return x            # ✅ gerçek implementasyon

# 🎯 Mimari öneri:
# - Overload imzalarını tek blok halinde tanımla.
# - Araya hiçbir ifade koyma.
# - Zincirin sonunda tek bir def ile gerçek fonksiyonu yaz.
# - Kodun okunabilirliğini korumak için overload sayısını minimumda tut, gerekmedikçe kullanma.


# ───────────────────────────────────────────────────────────────────────────────

# 🔹 Hızlı örnek akıl haritası (metinsel)
# @overload: statik sözleşme → input imzasına göre dönüş tipini kesinleştir.
# get_overloads: runtime’da overload imzalarını listele (introspection).
# clear_overloads: runtime’da overload imzalarını temizle (reload/yeniden bağlama).
# Literal/TypeVar/ParamSpec/Concatenate: overload ile birlikte daha ince taneli imza modelleme.
# singledispatch: runtime dispatch; @overload ile tamamlayıcı ama farklı amaç.
```
