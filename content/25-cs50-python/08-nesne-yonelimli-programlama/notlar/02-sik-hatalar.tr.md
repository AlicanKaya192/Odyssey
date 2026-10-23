Sınıflarla çalışırken en sık yapılan hatalar ve mesajları (Python 3.14'te,
bu bilgisayarda ölçüldü). Hata mesajının **son satırı** önce okunur.

## self'i unutmak

Metodun ilk parametresi her zaman nesnenin kendisi. Unutulursa Python
nesneyi `name`'e koyuyor ve argüman sayısı tutmuyor:

```python
class Student:
    def __init__(name, house):
        self.name = name
        self.house = house


student = Student("Harry", "Gryffindor")
```

```text
$ python student.py
Traceback (most recent call last):
  File "student.py", line 7, in <module>
    student = Student("Harry", "Gryffindor")
TypeError: Student.__init__() takes 2 positional arguments but 3 were given
```

"2 alıyor ama 3 verildi": senin iki argümanın ve Python'un kendiliğinden
verdiği nesne. Çözüm `def __init__(self, name, house):`.

## self. olmadan atamak

`name = name` yalnızca fonksiyonun içindeki yerel değişkene atar; nesneye
bir şey yazılmaz:

```python
class Student:
    def __init__(self, name, house):
        name = name
        house = house


student = Student("Harry", "Gryffindor")
print(student.name)
```

```text
$ python student.py
Traceback (most recent call last):
  File "student.py", line 8, in <module>
    print(student.name)
          ^^^^^^^^^^^^
AttributeError: 'Student' object has no attribute 'name'
```

Nesnede saklanacak her değer `self.name = name` diye yazılır.

## Özellikle aynı adlı değişken

Alıcı `self.house`'u döndürüyor; ama `self.house` alıcının kendisi. Ayarlayıcı
da `self.house = ...` ile kendini çağırıyor ve bu sonsuza kadar sürüyor:

```python
class Student:
    def __init__(self, house):
        self.house = house

    @property
    def house(self):
        return self.house

    @house.setter
    def house(self, house):
        self.house = house


student = Student("Gryffindor")
```

```text
$ python student.py
Traceback (most recent call last):
  File "student.py", line 14, in <module>
    student = Student("Gryffindor")
  File "student.py", line 3, in __init__
    self.house = house
    ^^^^^^^^^^
  File "student.py", line 11, in house
    self.house = house
    ^^^^^^^^^^
  File "student.py", line 11, in house
    self.house = house
    ^^^^^^^^^^
  File "student.py", line 11, in house
    self.house = house
    ^^^^^^^^^^
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```

Değeri farklı adlı bir örnek değişkeninde tut: `self._house`.

## __str__'de print

`__str__` bir dize **döndürmeli**. `print` ile yazıp hiçbir şey döndürmezse
`None` döner:

```python
class Student:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        print(f"Student {self.name}")


student = Student("Harry")
print(student)
```

```text
$ python student.py
Student Harry
Traceback (most recent call last):
  File "student.py", line 10, in <module>
    print(student)
    ~~~~~^^^^^^^^^
TypeError: __str__ returned non-string (type NoneType)
```

## Süsleyicisiz sınıf metodu

`@classmethod` yazılmazsa `sort` sıradan bir metot olur ve `Hat.sort("Harry")`
`"Harry"`'yi `cls`'ye koyar; `name` eksik kalır:

```python
class Hat:
    houses = ["Gryffindor", "Slytherin"]

    def sort(cls, name):
        print(name, "is in", cls.houses[0])


Hat.sort("Harry")
```

```text
$ python hat.py
Traceback (most recent call last):
  File "hat.py", line 8, in <module>
    Hat.sort("Harry")
    ~~~~~~~~^^^^^^^^^
TypeError: Hat.sort() missing 1 required positional argument: 'name'
```

## super().__init__'i unutmak

Alt sınıfın kendi `__init__`'i varsa üst sınıfınki kendiliğinden
çağrılmaz; adı atayan kod hiç çalışmıyor:

```python
class Wizard:
    def __init__(self, name):
        self.name = name


class Student(Wizard):
    def __init__(self, name, house):
        self.house = house


student = Student("Harry", "Gryffindor")
print(student.name)
```

```text
$ python wizard.py
Traceback (most recent call last):
  File "wizard.py", line 12, in <module>
    print(student.name)
          ^^^^^^^^^^^^
AttributeError: 'Student' object has no attribute 'name'
```

Alt sınıfın `__init__`'inin başına `super().__init__(name)`.

## Paylaşılan sınıf listesi

Sınıfın gövdesindeki değişken **bütün nesnelerin ortak** değişkeni. Liste gibi
değiştirilebilir bir değerse bir nesneye eklenen herkese eklenmiş olur:

```python
class Student:
    courses = []

    def __init__(self, name):
        self.name = name


harry = Student("Harry")
hermione = Student("Hermione")
harry.courses.append("Potions")
print(hermione.courses)
```

```text
$ python student.py
['Potions']
```

Her nesnenin kendi listesi olacaksa liste `__init__`'te oluşturulur:

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.courses = []


harry = Student("Harry")
hermione = Student("Hermione")
harry.courses.append("Potions")
print(hermione.courses)
```

```text
$ python student.py
[]
```

## Demeti değiştirmeye çalışmak

`return name, house` bir demet döndürür; `student[1] = ...` `TypeError: 'tuple'
object does not support item assignment` verir. Değişecekse liste, sözlük ya
da sınıf.
