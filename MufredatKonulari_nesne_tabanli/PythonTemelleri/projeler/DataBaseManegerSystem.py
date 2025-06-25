from collections.abc import Generator,MutableMapping
from ast import literal_eval
from time import clock_settime


class AccessorysFunctions:


    @staticmethod
    def user_contol(get_class_and_fields_func):
        _, new_data = get_class_and_fields_func # --> HATA BURDA ÇAĞRILMIYOR AMA ÇAĞRILDIĞIND
        for record in AccessorysFunctions.file_to_mapping():
            if all(record.get(k) == v for k, v in new_data.items()):
                raise ValueError("⚠️ Kullanıcı zaten sistemde kayıtlı!")
        return True

    def get_class_and_fields(self,*args,**kwargs) -> tuple:
        cls = self.__class__
        fields = {getattr(cls,key):value for key, value in kwargs.items()}
        return cls,fields

    @staticmethod
    def file_to_mapping() -> Generator[dict,None,None]:
        for line_str in AccessorysFunctions._file(flag="r"):
            dict_part = line_str[line_str.find("(") + 1: line_str.rfind(")")]
            try:
                yield literal_eval(dict_part)
            except Exception as e:
                print(f"Satır işlenemedi: {line_str} – {e}")

    def mapping_to_file(self,**mapping:MutableMapping):
        print("mapping_to_file >> ",self)
        AccessorysFunctions._file(flag="a",write_mapping_object=self.__repr__())


    @staticmethod
    def _file(*,path="data2.txt",flag="a",encoding="utf-8",write_mapping_object=None):
        def _write_func(file,write_object,/):
            file.write(write_object)
            print("başarıyla yazıldı")

        def _read_func(file,/,*args,**kwargs):
            try:
                for line in iter(file.readline, ""):
                    yield line
            finally:
                file.close()

        functions = {"a":_write_func,"r":_read_func}

        try:
            f=  open(path,flag,encoding=encoding)
            return  functions[flag](f,write_mapping_object)

        except FileNotFoundError:
            raise FileNotFoundError(f"File {path} not found.")
        except PermissionError:
            raise PermissionError(f"File {path} permission denied.")


class Decorators:
    __slots__ = ()
    @staticmethod
    def control_decorator(func):
        def chech_field(self,cls,fields):
            result = all(isinstance(key,Field) for key in fields)

            return result

        def check_type(self,cls,fields):
            result = all(isinstance(value, field.get) for field, value in fields.items())
            return result

        def wrapper(self, *args, **kwargs):
            cls, fields = (fu:=AccessorysFunctions.get_class_and_fields)(self,*args, **kwargs)

            if check_type(self, cls, fields) and chech_field(self, cls, fields):
                try:
                    AccessorysFunctions.user_contol(fu)  # Eğer kullanıcı varsa hata fırlatacak
                except ValueError as e:
                    print(e)
                    return None

                func(self, *args, **kwargs)
                AccessorysFunctions.mapping_to_file(self, **kwargs)

            return None
        return wrapper



class Field:
    __slots__ = ("_dtpe",)
    def __init__(self,dtpe):
        if isinstance(dtpe,type):
            self._dtpe = dtpe
        else:
            raise TypeError(f"{dtpe.__repr__()} is invalid type")
    @property
    def get(self):
        return self._dtpe

class Model:
    __slots__ = ("_data",)
    @Decorators.control_decorator
    def __init__(self,**kwargs):
        self._data = kwargs

    def __repr__(self):
        return f"{self.__class__.__name__}({self._data})\n"

class User(Model):
    name = Field(str)
    age = Field(int)
    mother_name = Field(str)
    country = Field(str)
    city = Field(str)
    mari = Field(bool)

#-------------------------------------------------------------
user1 = User(name="demir",age=20,mother_name="aslı",country="Turkey",city="Istanbul",mari=False)




