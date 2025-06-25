# -*- coding: utf-8 -*-
import random
import re 
import string
from collections.abc import Generator,Iterator,Hashable
from ast import literal_eval



IL_KODLARI = {
    "01": "Adana",
    "02": "Adıyaman",
    "03": "Afyonkarahisar",
    "04": "Ağrı",
    "05": "Amasya",
    "06": "Ankara",
    "07": "Antalya",
    "08": "Artvin",
    "09": "Aydın",
    "10": "Balıkesir",
    "11": "Bilecik",
    "12": "Bingöl",
    "13": "Bitlis",
    "14": "Bolu",
    "15": "Burdur",
    "16": "Bursa",
    "17": "Çanakkale",
    "18": "Çankırı",
    "19": "Çorum",
    "20": "Denizli",
    "21": "Diyarbakır",
    "22": "Edirne",
    "23": "Elazığ",
    "24": "Erzincan",
    "25": "Erzurum",
    "26": "Eskişehir",
    "27": "Gaziantep",
    "28": "Giresun",
    "29": "Gümüşhane",
    "30": "Hakkari",
    "31": "Hatay",
    "32": "Isparta",
    "33": "Mersin",
    "34": "İstanbul",
    "35": "İzmir",
    "36": "Kars",
    "37": "Kastamonu",
    "38": "Kayseri",
    "39": "Kırklareli",
    "40": "Kırşehir",
    "41": "Kocaeli",
    "42": "Konya",
    "43": "Kütahya",
    "44": "Malatya",
    "45": "Manisa",
    "46": "Kahramanmaraş",
    "47": "Mardin",
    "48": "Muğla",
    "49": "Muş",
    "50": "Nevşehir",
    "51": "Niğde",
    "52": "Ordu",
    "53": "Rize",
    "54": "Sakarya",
    "55": "Samsun",
    "56": "Siirt",
    "57": "Sinop",
    "58": "Sivas",
    "59": "Tekirdağ",
    "60": "Tokat",
    "61": "Trabzon",
    "62": "Tunceli",
    "63": "Şanlıurfa",
    "64": "Uşak",
    "65": "Van",
    "66": "Yozgat",
    "67": "Zonguldak",
    "68": "Aksaray",
    "69": "Bayburt",
    "70": "Karaman",
    "71": "Kırıkkale",
    "72": "Batman",
    "73": "Şırnak",
    "74": "Bartın",
    "75": "Ardahan",
    "76": "Iğdır",
    "77": "Yalova",
    "78": "Karabük",
    "79": "Kilis",
    "80": "Osmaniye",
    "81": "Düzce"
}


class Functions:
    @staticmethod
    def parse_all_lines(kayit) -> Generator[dict, None, None]:
        for line in kayit.dataObject.base_pull(kayit.dataObject):
            try:

                yield literal_eval(line)
            except Exception as e:
                print(f"Satır işlenemedi: {line} – {e}")

    @staticmethod
    def checklicense(license: str, *, regex: re.Pattern[str]) -> dict:
        license_info = None
        if match := regex.fullmatch(license):
            license_info = match.groupdict(default="????")
        return license_info

    @staticmethod
    def compile_regex(regex: str) -> re.Pattern[str]:
        return re.compile(regex)

class Decorators:

    # DATABASE GLOBAL DECORATOR:
    @staticmethod
    def control_wrapper(fonk):
        def wrapper(self, do, *args, **kwargs):
            if not do.ID == self.ID:
                return print("yetkisiz erisim")
            return fonk(self, *args, **kwargs)

        return wrapper


    # KAYİT CLASS GLOBAL DECORATOR:
    @staticmethod
    def control_wrapper_kayit(mode):

            def add_control(self, arac):
                return not any(arac.plaka in line for line in Functions.parse_all_lines(self))

            def check_control(self, plaka: str, *args):
                return any(plaka in line for line in Functions.parse_all_lines(self))

            control_functions = {
                "add": add_control,
                "check": check_control
            }

            def decorator(fonk):
                def sarmal(self, *args):
                    control_func = control_functions[mode]

                    result = control_func(self, *args)
                    if not result:
                        return f"--> {''.join(f'{deger}' for deger in args)} Error"
                    return fonk(self, *args)

                return sarmal

            return decorator



# DATABASE GLOBAL FUNCTION:
def open_data(class_instance:object, flag:str, key:Hashable=None, value:object=None,*, encode="utf-8", mode="bool"):
    def return_generator(file) -> Generator[str,None,None]:
        try:
            for line in iter(file.readline,""):
                yield line
        finally:
            file.close()        

    def return_bool(file):
        try:
            file.write(class_instance.format_repr(key,value)) 
        except Exception as e:
            print(f"Hata oluştu: {e}")
            return False
        else:
            return True
        finally:
            file.close()

    choose =  {"gen":return_generator, "bool":return_bool}

    file = open(class_instance.path,flag,encoding=encode)
    return choose[mode](file)
    
# GLOBAL FUNCTIONS:

P = Functions.compile_regex(r"(?P<il>\d{2})\s?(?P<harfler>[A-Z]{1,3})\s?(?P<sayilar>\d{2,4})")


# CLASSES:
class MainDataBase:

    __slots__ = ("path","ID")

    def __init__(self,path:str):
        super().__setattr__("path", path)
        super().__setattr__("ID","".join(random.choices(string.ascii_letters,k=random.randint(8,11))))
    
    def __setattr__(self, key, value):
        raise TypeError(f"{key} Değiştirilemez !")



    @Decorators.control_wrapper
    def base_pull(self) -> Generator[Iterator,None,None]:
            yield from open_data(self,"r",mode="gen")

    @Decorators.control_wrapper
    def base_push(self,key,value):
        open_data(self,"a",key,value)
            
    def override_push(self,key,value):
        open_data(self,"w",key,value)

class AracDataBase(MainDataBase):

    __slots__ = MainDataBase.__slots__

    def format_repr(self,plaka:str,arac:object):
        return f"{{'{plaka}': {arac.return_values()}}}\n"

class Arac:

    __slots__ = ("marka","model","yil","plaka","ceza")

    def __init__(self,marka,model,yil,plaka, ceza):
        self.marka = marka 
        self.model = model
        self.yil = yil 
        self.plaka = plaka
        self.ceza = ceza

    @classmethod
    def founder(cls, marka, model, yil, plaka, ceza):
        if Functions.checklicense(plaka,regex=P):
           return  cls(marka,model,yil,plaka,ceza)
        raise ValueError(f" plaka numarası > {plaka} HATALI")

    def return_values(self) -> dict:
        return {attr:getattr(self,attr) for attr in self.__slots__}
    
    def __repr__(self):
        return f"Arac({self.return_values()!r})"
    
class Kayıt:

    __slots__ = ("aracListesi","dataObject")  

    def __init__(self, data_object: AracDataBase):
        self.aracListesi = {} #geçersiz kılıncak
        self.dataObject = data_object
        
    def __setitem__(self,ap,arac:Arac):
        self.dataObject.base_push(self.dataObject,ap,arac)
    
    def __str__(self):
        return "\n\n".join(
        f"{plaka}:\n  " + "\n  ".join(f"{k}: {v}" for k, v in arac.items())
        for line in Functions.parse_all_lines(self)
        for plaka, arac in line.items()
        )

    @Decorators.control_wrapper_kayit("add")
    def new(self, arac: Arac):
        self.__setitem__(arac.plaka, arac)


    @Decorators.control_wrapper_kayit("check") #
    def check_license(self, plaka: str):
        veri = self.__str__().split("\n\n")
        print(repr(veri))
        return "".join([satır for satır in veri if plaka in satır])
       
          
    @staticmethod
    def random_license_generator() -> str:
        il = f"{random.randint(1,81):02}"
        harfler = ''.join(random.choices(string.ascii_uppercase, k=random.randint(2,4)))
        sayilar = ''.join(random.choices(string.digits, k=random.randint(1,4)))
        return f"{il}{harfler}{sayilar}"

    @Decorators.control_wrapper_kayit("check")
    def penalty(self, plaka: str):
        buffer = []

        for arac in Functions.parse_all_lines(self):
            if plaka in arac:
                arac["ceza"] = True
                buffer.append()


# Kullanım: #############################################################################################################################
araba = Arac("BMW", "I5", "2021", "06KSY63", None)
araba2 = Arac("Mercedes", "q20", "2011", "34BGS98", None)

data = AracDataBase(r"data.txt")
data2 = AracDataBase(r"data.txt")
kayit = Kayıt(data)



kayit.new(araba)
kayit.new(araba2)
araba3 = Arac("volvo", None,"2012",kayit.random_license_generator(), None)
print(kayit)
print(
    kayit.random_license_generator()
)

kayit.new(araba3)

