from collections.abc import Callable
from inspect import isfunction,Parameter
from functools import wraps

class Singledispatchproperty:
    def __init__(self,func,fget=False):
        self.__default_func = func
        self.registry = {}
        self.fget  = fget
    def register(self, typ):
        def wrapper(func):
            self.fget = True
            self.registry[typ] = func
            return func
        return wrapper

    def dispatch(self, typ):
        return self.registry.get(typ, self.__default_func)

    def __get__(self,instance, owner):
        if not self.fget:
            raise ValueError
        return self.dispatch(instance.target_object.__class__)(instance)



class Debugdecoratos:
    @staticmethod
    def convert_to_string(func:Callable):
        if not isfunction(func):
            raise TypeError("func must be a function")

        @wraps(func) # orjinal fonksiyonun metadatası korunur
        def wrapper(self, written_object:object, *args, **kwargs):
                """verilen objeyi(ŞUANDA BELLİ DEĞİL) string formata çevirir
                (ŞUAN BUNU __repr__ KULLANARAK YAPMAYI DÜŞÜNÜYORUM AMA DEĞİŞEBİLİR)"""
                ...
                return func(written_object, *args, **kwargs)
        return wrapper

class Debug:

    __slots__= ("__log_to_file","__file_path","target_object")

    def __init__(self,target_object:object,/,*, log_to_file:bool= False, file_path:str= None):
        """
        :param log_to_file: True ise çıktı dosyaya yazılır, False ise konsola yazılır.
        :param file_path: log_to_file=True ise, yazılacak dosya yolu.
        """
        self.__log_to_file = log_to_file
        self.__file_path = file_path or "log.txt"
        self.target_object = target_object

    def log(self,wobj):
        if self.__log_to_file:
            self.write_to_file(self,wobj)
        else:
            raise ValueError(f"log_to_file param is >>> {self.__log_to_file}")

    @Singledispatchproperty
    def analyze_object(self):
        self.write_to_file(r:=self.__return_basic_attributes(self.target_object))
        return r
    @analyze_object.register(type)
    def _(self):
        self.write_to_file(r:=self.__analyze_callable(self.target_object))
        return r

    @staticmethod
    def __return_basic_attributes(sto) -> str:
        obj = sto
        cls = obj.__class__
        mro = cls.__mro__
        output = []

        # 🔍 1. Objeye ait local attribute sözlüğü
        output.append("🧠 [Instance __dict__]:")
        if hasattr(obj, '__dict__'):
            for k, v in obj.__dict__.items():
                output.append(f"\t{k} = ({v})")
        else:
            output.append("\t<No __dict__ found>")

        # 🏷️ 2. Objeyi oluşturan sınıf
        output.append("\n🏷️ [Type]:")
        output.append(f"\t{cls.__name__}")

        # 🧬 3. MRO zinciri (inheritance sırası)
        output.append("\n🧬 [Method Resolution Order (MRO)]:")
        for num, base in enumerate(mro, 1):
            output.append(f"\t{num}.{base.__name__}")

        # 🧩 4. İlk üst sınıfın attribute sözlüğü
        if len(mro) > 1:
            output.append(f"\n📦 [Superclass '{mro[1].__name__}' __dict__]:")
            for k, v in mro[1].__dict__.items():
                output.append(f"\t{k} -> ({v})")
        else:
            output.append("\n📦 [No superclass]")

        # ⚙️ 5. type(type(obj)) → metaclass
        output.append("\n⚙️ [Metaclass]:")
        output.append(f"\t{type(cls)}")

        return "\n".join(output)

    @staticmethod
    def __analyze_callable(sto):
        from inspect import isfunction, ismethod, isclass, signature, getsource

        output = ["📞 Callable Object Analysis:"]

        if isfunction(sto):
            output.append("🔹 Type: Function")
        elif ismethod(sto):
            output.append("🔹 Type: Method")
        elif isclass(sto):
            output.append("🔹 Type: Class (might be callable via __init__)")
        elif hasattr(sto, '__call__'):
            output.append("🔹 Type: Callable Object (has __call__)")
        else:
            output.append("🔸 Not callable?")
            return "\n".join(output)

        output.append(f"📝 Signature: {signature(sto)}")
        doc = getattr(sto, '__doc__', '')
        if doc:
            output.append(f"📚 Docstring: {doc.strip()}")
        annotations = getattr(sto, '__annotations__', {})
        if annotations:
            output.append(f"🔍 Annotations: {annotations}")
        output.append(Debug.__return_basic_attributes(sto))
        # Source if available
        try:
            output.append("🧾 Source:")
            output.append(getsource(sto))
        except Exception:
            output.append("❌ Source not available")

        return "\n".join(output)

    # @Debugdecoratos.convert_to_string
    def write_to_file(self, text: str):
        """hedef dosyayı yazmak amaçlı açar
         :text: string argüman ister """
        with open(self.__file_path, "a", encoding="utf-8") as f:
            f.write(text)


    def single_statement(self,obj):
        local = {}
        codes = obj.strip().splitlines(True)
        returns = []
        for i, line in enumerate(codes, start=1):
            try:
                exec(line, {}, local)
                returns.append(f"[{i}] ✅ Başarılı: {line}\n")
            except Exception as e:
                returns.append(f"[{i}] ❌ Hata: {line} -> {type(e).__name__}: {e}\n")

        # Son durumda hangi değişkenler üretildi
        if local:
            returns.append("📦 Yerel Değişkenler:\n")
            for name, value in local.items():
                returns.append(f"\t - {name} = {value!r}")
        self.write_to_file("\n".join(returns))



d = Debug(None)
d.single_statement("x=10")
d.analyze_object


