# Nesne Yönelimli Programlama

CS50 Python'un dokuzuncu haftası. Videoyu **Video** sekmesinden
izleyebilirsin; bu sayfa dersin yazılı hâli. Programlamada problem
çözmenin farklı **paradigmaları** (yaklaşımları) var. Şimdiye kadar büyük
ölçüde **prosedürel** kod yazdık: fonksiyonlar, yukarıdan aşağıya adım adım
işler. `lambda` ile fonksiyonları başka fonksiyonlara verdiğimizde
**fonksiyonel** programlamaya da dokunduk. Bu hafta üçüncüsü: **nesne
yönelimli programlama** (object-oriented programming, OOP). Programlar
uzadıkça, büyüdükçe ve karmaşıklaştıkça karşına çıkan problemlere oldukça
ikna edici bir çözüm.

## Birden fazla değer döndürmek: demet

Harry Potter dünyasından bir öğrencinin adını ve binasını (house) alan bir
program, `student.py`. Bir öğrenciyi tek fonksiyonla almak istiyoruz; ama
elimizde iki değer var. Python'da virgülle ikisini birden döndürebilir,
dönüşte de virgülle iki değişkene açabilirsin:

```python
def main():
    name, house = get_student()
    print(f"{name} from {house}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return name, house


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

Burada aslında **tek** bir değer dönüyor: bir **demet** (tuple). Demet,
listeye benzeyen bir değerler topluluğu; virgül tek başına demet kurar,
istersen parantezle açıkça yazarsın: `(name, house)`. Demeti açmadan tek
değişkende tutup içine listedeki gibi konumla bakabilirsin:

```python
def main():
    student = get_student()
    print(f"{student[0]} from {student[1]}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return (name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

## Demet değiştirilemez

Filmlerde Padma Gryffindor'da, kitaplarda Ravenclaw'da. Kullanıcı Padma
yazarsa binasını düzeltelim:

```python
def main():
    student = get_student()
    if student[0] == "Padma":
        student[1] = "Ravenclaw"
    print(f"{student[0]} from {student[1]}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return (name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Padma
House: Gryffindor
Traceback (most recent call last):
  File "student.py", line 15, in <module>
    main()
    ~~~~^^
  File "student.py", line 4, in main
    student[1] = "Ravenclaw"
    ~~~~~~~^^^
TypeError: 'tuple' object does not support item assignment
```

Demet **değiştirilemez** (immutable): oluşturduktan sonra içindeki bir
konuma yeni değer atanamaz. Bu bir hata değil, demetin tasarımı. Bir
değerin değişmemesi gerekiyorsa onu değiştirilebilen bir türde tutmamak,
senin ya da bir meslektaşının ileride yapacağı hatanın önünü keser.

Değiştirmek istiyorsan liste kullan: `get_student`'ta yalnızca
`return [name, house]` yazınca kod çalışıyor.

```text
$ python student.py
Name: Padma
House: Gryffindor
Padma from Ravenclaw
```

Değer **oluştururken** köşeli parantez liste, parantez demet demektir; ama
**içine bakarken** ikisinde de köşeli parantez kullanılır: `student[0]`.

## Sözlük

`student[0]`'ın ad, `student[1]`'in bina olduğunu hatırlamak gerekiyor; alan
sayısı arttıkça bu karışır. Sözlük her değere bir ad verir:

```python
def main():
    student = get_student()
    if student["name"] == "Padma":
        student["house"] = "Ravenclaw"
    print(f"{student['name']} from {student['house']}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return {"name": name, "house": house}


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Padma
House: Gryffindor
Padma from Ravenclaw
```

f-string'in içinde anahtarı tek tırnakla yazdık, dışı çift tırnak.
Videodaki Python'da içeride de çift tırnak kullanmak sözdizimi hatasıydı;
**Python 3.12'den beri** f-string'in içinde aynı tırnak kullanılabiliyor
(bu bilgisayardaki 3.14'te ölçüldü):

```python
student = {"name": "Harry", "house": "Gryffindor"}
print(f"{student["name"]} from {student["house"]}")
```

```text
$ python student.py
Harry from Gryffindor
```

Yine de iki tırnağı ayırmak okumayı kolaylaştırır.

## Sınıflar

Demet, liste, sözlük genel amaçlı türler. Python'da bir `Student` türü olsa
bu tartışmaya gerek kalmazdı. Python bize bunun yerine kendi türümüzü
yaratmanın yolunu veriyor: **sınıf** (class). Sınıf bir **plan**, bir
**kalıp**: o kalıpla oluşturduğun her değer aynı yapıda olur.

```python
class Student:
    ...


def main():
    student = get_student()
    print(f"{student.name} from {student.house}")


def get_student():
    student = Student()
    student.name = input("Name: ")
    student.house = input("House: ")
    return student


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

- `class Student:` yeni bir tür tanımlar. Gelenek: sınıf adı büyük harfle
  başlar. `...` "gövdeyi sonra yazacağım" diyen geçerli bir yer tutucu.
- `Student()` bu sınıftan bir **nesne** (object) oluşturur. Nesneye sınıfın
  bir **örneği** (instance) de denir: sınıf evin planıysa nesne o planla
  yapılmış belirli bir ev.
- `student.name = ...` nesneye bir **nitelik** (attribute) ekler. Nokta,
  modüllerde olduğu gibi "bunun içindeki şu" demek.

## __init__ ve self

Nitelikleri dışarıdan tek tek eklemek dağınık. Nesne oluşturulurken
değerleri bir kerede verelim: `Student(name, house)`. Bunun için sınıfa özel
bir metot yazılır. **Metot** (method), sınıfın içindeki fonksiyondur.

```python
class Student:
    def __init__(self, name, house):
        self.name = name
        self.house = house


def main():
    student = get_student()
    print(f"{student.name} from {student.house}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

- `Student(name, house)` bir **kurucu çağrısı** (constructor call). Python
  önce bellekte boş bir nesne oluşturur, sonra onu başlatmak için
  `__init__`'i kendiliğinden çağırır. Başındaki ve sonundaki çift alt
  çizgiye **dunder** (double underscore) denir.
- `__init__`'in ilk parametresi `self`: az önce oluşturulan nesnenin
  kendisi. Çağırırken onu sen vermezsin, Python verir; `Student("Harry",
  "Gryffindor")` iki argümanla çağrılır, `__init__` üç parametre alır.
- `self.name = name` değeri o nesnenin içinde saklar. Nesnenin içindeki bu
  değişkenlere **örnek değişkeni** (instance variable) denir.

Sınıfın bir sözlükten farkı burada başlıyor: içeri neyin gireceğini sen
denetleyebilirsin.

## Hata yükseltmek: raise

Ad boşsa ya da bina dört Hogwarts binasından biri değilse öğrenci hiç
oluşturulmamalı. `print` ile uyarmak yetmez (program devam eder),
`sys.exit` ise bütün programı kapatır. Üstelik `__init__` çalıştığında
nesne zaten var; `None` döndürmek için geç. Doğru yol bir **istisna**
yükseltmek (raise): şimdiye kadar Python'un yükselttiği `ValueError`'ları
yakaladık, şimdi kendimiz yükseltiyoruz.

```python
class Student:
    def __init__(self, name, house):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house


def main():
    student = get_student()
    print(f"{student.name} from {student.house}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

Harry, büyüdüğü evin adresini yazarsa:

```text
$ python student.py
Name: Harry
House: Number Four, Privet Drive
Traceback (most recent call last):
  File "student.py", line 23, in <module>
    main()
    ~~~~^^
  File "student.py", line 12, in main
    student = get_student()
  File "student.py", line 19, in get_student
    return Student(name, house)
  File "student.py", line 6, in __init__
    raise ValueError("Invalid house")
ValueError: Invalid house
```

`raise ValueError("Invalid house")` ile mesajı da biz veriyoruz. Öğrenciyi
oluşturan kod isterse bunu her zamanki `try` / `except ValueError` ile
yakalayabilir.

## __str__

Öğrenciyi doğrudan yazdırırsak:

```python
class Student:
    def __init__(self, name, house):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house


def main():
    student = get_student()
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
<__main__.Student object at 0x...>
```

Varsayılan dize gösterimi nesnenin türünü ve bellekteki yerini (`0x...`, her
çalıştırmada başka) söylüyor. **`__str__`** özel metodunu tanımlarsan, bir
fonksiyon (`print` gibi) nesneni dize olarak görmek istediğinde Python onu
kendiliğinden çağırır:

```python
class Student:
    def __init__(self, name, house):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"


def main():
    student = get_student()
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Draco
House: Slytherin
Draco from Slytherin
```

(`__repr__` de var: geliştiriciler için, genelde daha ayrıntılı gösterim.)

## Kendi metotlarımız

Özel metotların yanında kendi metotlarımızı da yazabiliriz. Öğrencilerin bir
**patronusu** var; `charm` metodu ona uygun bir emoji döndürsün. Kendi
metodunun da ilk parametresi `self`:

```python
class Student:
    def __init__(self, name, house, patronus):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house
        self.patronus = patronus

    def __str__(self):
        return f"{self.name} from {self.house}"

    def charm(self):
        match self.patronus:
            case "Stag":
                return "🐴"
            case "Otter":
                return "🦦"
            case "Jack Russell terrier":
                return "🐶"
            case _:
                return "🪄"


def main():
    student = get_student()
    print("Expecto Patronum!")
    print(student.charm())


def get_student():
    name = input("Name: ")
    house = input("House: ")
    patronus = input("Patronus: ")
    return Student(name, house, patronus)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Patronus: Stag
Expecto Patronum!
🐴
```

Patronusu olmayan Draco:

```text
$ python student.py
Name: Draco
House: Slytherin
Patronus: 
Expecto Patronum!
🪄
```

Sınıf yalnızca veriyi (nitelikler) değil, o veriyle yapılan işleri
(metotlar) da bir arada tutuyor.

## Özellikler

`__init__`'teki denetim yalnızca nesne **oluşturulurken** çalışıyor. Sonra
niteliği değiştirmeye kimse engel olmuyor:

```python
class Student:
    def __init__(self, name, house):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"


def main():
    student = get_student()
    student.house = "Number Four, Privet Drive"
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Number Four, Privet Drive
```

**Özellik** (property), denetimi atamaya da taşır. Niteliğin okunması bir
**alıcı** (getter), atanması bir **ayarlayıcı** (setter) metodundan geçer:

```python
class Student:
    def __init__(self, name, house):
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"

    # Getter
    @property
    def name(self):
        return self._name

    # Setter
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Missing name")
        self._name = name

    @property
    def house(self):
        return self._house

    @house.setter
    def house(self, house):
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self._house = house


def main():
    student = get_student()
    student.house = "Number Four, Privet Drive"
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Traceback (most recent call last):
  File "student.py", line 45, in <module>
    main()
    ~~~~^^
  File "student.py", line 34, in main
    student.house = "Number Four, Privet Drive"
    ^^^^^^^^^^^^^
  File "student.py", line 28, in house
    raise ValueError("Invalid house")
ValueError: Invalid house
```

- `@property` bir **süsleyici** (decorator): altındaki fonksiyonun
  davranışını değiştiren bir fonksiyon. Burada `house` metodunu alıcı yapıyor;
  `student.house` artık bu metodu çağırıyor.
- `@house.setter` aynı adlı ikinci metodu ayarlayıcı yapıyor;
  `student.house = ...` artık onu çağırıyor ve geçersiz değerde
  `ValueError` yükseliyor.
- Değerin kendisi `self._house`'ta. Örnek değişkeni de `house` adını
  taşısaydı özellikle çakışırdı; gelenek, başına alt çizgi koymak.
- `__init__`'te `self.house = house` yazdık, alt çizgisiz: o atama da
  ayarlayıcıdan geçiyor, denetim tek yerde.

Ad boş bırakılırsa denetim yine ayarlayıcıda, ama bu kez `__init__`
çalışırken:

```text
$ python student.py
Name: 
House: Gryffindor
Traceback (most recent call last):
  File "student.py", line 44, in <module>
    main()
    ~~~~^^
  File "student.py", line 33, in main
    student = get_student()
  File "student.py", line 40, in get_student
    return Student(name, house)
  File "student.py", line 3, in __init__
    self.name = name
    ^^^^^^^^^
  File "student.py", line 18, in name
    raise ValueError("Missing name")
ValueError: Missing name
```

Python'da Java gibi dillerdeki **özel** (private) değişken yok. Alt çizgili
değişkene doğrudan yazılırsa hiçbir şey engel olmuyor:

```python
class Student:
    def __init__(self, name, house):
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"

    # Getter
    @property
    def name(self):
        return self._name

    # Setter
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Missing name")
        self._name = name

    @property
    def house(self):
        return self._house

    @house.setter
    def house(self, house):
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self._house = house


def main():
    student = get_student()
    student._house = "Number Four, Privet Drive"
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Number Four, Privet Drive
```

Alt çizgi bir **gelenek**: "buna dokunma" demek. Bozarsan sorumluluk sende.

## Bildiğimiz türler de sınıf

`int`, `str`, `list`, `dict` hep birer sınıftı. `"hello".lower()` bir `str`
nesnesinin metodunu, `list.append` bir `list` nesnesinin metodunu çağırıyor.
`type` bir değerin sınıfını söyler, `type.py`:

```python
print(type(50))
print(type("hello, world"))
print(type([]))
print(type({}))
```

```text
$ python type.py
<class 'int'>
<class 'str'>
<class 'list'>
<class 'dict'>
```

Python'un yerleşik türleri küçük harfle başlıyor; kendi sınıflarında gelenek
büyük harf.

## Sınıf metotları ve sınıf değişkenleri

Seçmen Şapka (sorting hat) öğrencinin adını alıp onu bir binaya yerleştirsin,
`hat.py`. Önce şimdiye kadarki gibi: bir `Hat` nesnesi oluşturup metodunu
çağırıyoruz (`random.choice` rastgele bir bina seçiyor):

```python
import random


class Hat:
    def __init__(self):
        self.houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

    def sort(self, name):
        print(name, "is in", random.choice(self.houses))


hat = Hat()
hat.sort("Harry")
```

```text
$ python hat.py
Harry is in Hufflepuff
```

Ama Hogwarts'ta tek bir Seçmen Şapka var; birden çok şapka nesnesi
oluşturmanın anlamı yok. Bina listesi de belirli bir şapkanın değil, sınıfın
kendisinin:

```python
import random


class Hat:
    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

    @classmethod
    def sort(cls, name):
        print(name, "is in", random.choice(cls.houses))


Hat.sort("Harry")
```

```text
$ python hat.py
Harry is in Ravenclaw
```

- `houses` artık **sınıf değişkeni** (class variable): sınıfın içinde,
  `self` olmadan tanımlı; bütün nesneler aynı tek kopyayı paylaşır.
- `@classmethod` bir **sınıf metodu**: nesne oluşturmadan `Hat.sort(...)`
  diye çağrılır. İlk parametresi nesne değil sınıfın kendisi; gelenek
  olarak `cls` (`class` anahtar kelime olduğu için kullanılamıyor).
- Şimdiye kadarki metotlar **örnek metotları** (instance method):
  süsleyicisiz her metot öyledir.

Aynı fikir öğrenci programını da toparlıyor. `get_student` öğrenciyle
ilgili olduğu hâlde sınıfın dışındaydı; öğrenciyle ilgili her şey sınıfta
dursun:

```python
class Student:
    def __init__(self, name, house):
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"

    @classmethod
    def get(cls):
        name = input("Name: ")
        house = input("House: ")
        return cls(name, house)


def main():
    student = Student.get()
    print(student)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

`cls(name, house)` "bu sınıftan bir nesne oluştur" demek. `Student.get()`
nesne oluşturmadan çağrılabiliyor; yoksa bir öğrenci almak için önce bir
öğrenci gerekirdi.

Üçüncü bir tür daha var: `@staticmethod` ile **statik metot**; ne nesneyi ne
sınıfı alır. Bu derste kullanmıyoruz.

## Kalıtım

Öğrencilerin de profesörlerin de adı var, ikisinde de adın boş olmaması
gerekiyor. Aynı denetimi iki sınıfa kopyalamak yerine ortak kısmı bir üst
sınıfa alalım: ikisi de bir büyücü (wizard). `wizard.py`:

```python
class Wizard:
    def __init__(self, name):
        if not name:
            raise ValueError("Missing name")
        self.name = name


class Student(Wizard):
    def __init__(self, name, house):
        super().__init__(name)
        self.house = house


class Professor(Wizard):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject


wizard = Wizard("Albus")
student = Student("Harry", "Gryffindor")
professor = Professor("Severus", "Defense Against the Dark Arts")

print(wizard.name)
print(student.name, student.house)
print(professor.name, professor.subject)
print(isinstance(student, Wizard), isinstance(student, Professor))
```

```text
$ python wizard.py
Albus
Harry Gryffindor
Severus Defense Against the Dark Arts
True False
```

- `class Student(Wizard):` `Student`'ın `Wizard`'dan **miras aldığını**
  söylüyor (inheritance). `Student` bir **alt sınıf** (subclass), `Wizard`
  onun **üst sınıfı** (superclass).
- `super().__init__(name)` üst sınıfın `__init__`'ini çağırıyor: adın
  atanması ve denetimi `Wizard`'da, tek yerde. Alt sınıf yalnızca kendine
  özgü olanı (`house`, `subject`) ekliyor.
- `isinstance(student, Wizard)` doğru: her öğrenci bir büyücü.

İstisnalar da bir hiyerarşi; `ValueError`'ın üst sınıflarını sırasıyla
yazdıralım, `exceptions.py`:

```python
for cls in ValueError.__mro__:
    print(cls.__name__)
```

```text
$ python exceptions.py
ValueError
Exception
BaseException
object
```

`except Exception:` bu yüzden `ValueError`'ı da yakalar. Kendi istisnanı
yazacaksan sıfırdan değil, var olan birinden türetirsin:
`class HouseError(ValueError): ...`.

## İşleç aşırı yükleme

`+` her zaman toplama demek değil: dizeleri ve listeleri birleştiriyor. Bu
anlamı türün kendisi belirliyor ve kendi sınıfın için sen de
belirleyebilirsin: **işleç aşırı yükleme** (operator overloading).
Gringotts bankasındaki kasalar, `vault.py`; önce iki kasayı elle
topluyoruz:

```python
class Vault:
    def __init__(self, galleons=0, sickles=0, knuts=0):
        self.galleons = galleons
        self.sickles = sickles
        self.knuts = knuts

    def __str__(self):
        return f"{self.galleons} Galleons, {self.sickles} Sickles, {self.knuts} Knuts"


potter = Vault(100, 50, 25)
print(potter)

weasley = Vault(25, 50, 100)
print(weasley)

galleons = potter.galleons + weasley.galleons
sickles = potter.sickles + weasley.sickles
knuts = potter.knuts + weasley.knuts

total = Vault(galleons, sickles, knuts)
print(total)
```

```text
$ python vault.py
100 Galleons, 50 Sickles, 25 Knuts
25 Galleons, 50 Sickles, 100 Knuts
125 Galleons, 100 Sickles, 125 Knuts
```

Doğrudan `potter + weasley` yazsak Python iki kasanın nasıl toplanacağını
bilmiyor:

```python
class Vault:
    def __init__(self, galleons=0, sickles=0, knuts=0):
        self.galleons = galleons
        self.sickles = sickles
        self.knuts = knuts

    def __str__(self):
        return f"{self.galleons} Galleons, {self.sickles} Sickles, {self.knuts} Knuts"


potter = Vault(100, 50, 25)
weasley = Vault(25, 50, 100)
total = potter + weasley
```

```text
$ python vault.py
Traceback (most recent call last):
  File "vault.py", line 13, in <module>
    total = potter + weasley
            ~~~~~~~^~~~~~~~~
TypeError: unsupported operand type(s) for +: 'Vault' and 'Vault'
```

`__add__` özel metodu bunu öğretiyor. `a + b` yazıldığında Python
`a.__add__(b)`'yi çağırır: `self` soldaki işlenen, gelenek olarak `other`
sağdaki.

```python
class Vault:
    def __init__(self, galleons=0, sickles=0, knuts=0):
        self.galleons = galleons
        self.sickles = sickles
        self.knuts = knuts

    def __str__(self):
        return f"{self.galleons} Galleons, {self.sickles} Sickles, {self.knuts} Knuts"

    def __add__(self, other):
        galleons = self.galleons + other.galleons
        sickles = self.sickles + other.sickles
        knuts = self.knuts + other.knuts
        return Vault(galleons, sickles, knuts)


potter = Vault(100, 50, 25)
weasley = Vault(25, 50, 100)

total = potter + weasley
print(total)
```

```text
$ python vault.py
125 Galleons, 100 Sickles, 125 Knuts
```

`__sub__` (`-`), `__eq__` (`==`), `__lt__` (`<`) gibi pek çok işlecin özel
metodu var. Yeni işleç (yeni bir sembol) tanımlanamaz, yalnızca var olanlara
anlam verilir.

## Özet

- Demet `(a, b)` değiştirilemez, liste `[a, b]` değiştirilebilir; sözlük
  her değere bir ad verir.
- `class`, nesne, örnek, nitelik; `__init__` ve `self`
- `raise ValueError("...")`
- `__str__`, kendi metotların
- `@property`, `@x.setter`, alt çizgi geleneği
- Sınıf değişkeni, `@classmethod` ve `cls`
- Kalıtım: `class Student(Wizard):`, `super().__init__(...)`
- İşleç aşırı yükleme: `__add__`

Sınıf her zaman şart değil; kısa bir programda birkaç fonksiyon da iş görür.
Ama birbiriyle ilgili veri ve işlevleri, adı olan bir yerde toplamak, kod
büyüdükçe düzeni korumanın bir yolu.

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) dersinin 8. haftasından (ders notu ve problem seti) çevrilip uyarlanmıştır; örnekler ve alıştırmalar değiştirildi, problem seti CS50'nin check50'siyle değil Odyssey'nin denetimiyle sınanıyor. Özgün içerik ve bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
