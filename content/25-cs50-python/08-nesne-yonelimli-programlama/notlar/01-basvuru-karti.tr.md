Hafta 8'de geçen her şey tek sayfada.

## Demet, liste, sözlük

| Yazım | Ne yapar |
|---|---|
| `return name, house` | bir demet döndürür (virgül demeti kurar) |
| `name, house = get_student()` | demeti iki değişkene açar |
| `(a, b)` / `[a, b]` | demet (değiştirilemez) / liste (değiştirilebilir) |
| `t[0] = x` | demette `TypeError` |
| `{"name": n, "house": h}` | sözlük: her değerin bir adı var |

## Sınıf ve nesne

| Yazım | Ne yapar |
|---|---|
| `class Student:` | yeni bir tür (sınıf); ad büyük harfle başlar |
| `student = Student("Harry", "Gryffindor")` | nesne (örnek) oluşturur; kurucu çağrısı |
| `def __init__(self, name, house):` | nesneyi başlatır; Python kendiliğinden çağırır |
| `self.name = name` | örnek değişkeni (nitelik) |
| `student.name` | niteliği okur |
| `raise ValueError("Invalid house")` | geçersiz değerde hata yükseltir |
| `def __str__(self): return ...` | `print(student)` ve `str(student)` bunu kullanır |
| `def charm(self): ...` | kendi metodun; ilk parametre `self` |

## Özellikler

```python
@property
def house(self):          # alıcı: student.house
    return self._house

@house.setter
def house(self, house):   # ayarlayıcı: student.house = ...
    if house not in HOUSES:
        raise ValueError("Invalid house")
    self._house = house
```

- Değer `self._house`'ta; özellikle aynı adı taşıyamaz.
- `__init__`'te `self.house = house` (alt çizgisiz): atama ayarlayıcıdan
  geçer.
- Alt çizgi bir gelenek, kilit değil: `student._house = ...` engellenmez.

## Sınıf düzeyi

| Yazım | Ne yapar |
|---|---|
| `houses = [...]` (sınıfın gövdesinde) | sınıf değişkeni: bütün nesneler paylaşır |
| `@classmethod` + `def sort(cls, name):` | sınıf metodu; `Hat.sort("Harry")` |
| `return cls(name, house)` | sınıf metodunun içinden nesne oluşturur |
| `@staticmethod` | ne nesneyi ne sınıfı alan metot |

## Kalıtım

| Yazım | Ne yapar |
|---|---|
| `class Student(Wizard):` | `Student`, `Wizard`'ın alt sınıfı |
| `super().__init__(name)` | üst sınıfın `__init__`'ini çağırır |
| `isinstance(student, Wizard)` | nesne bu sınıftan (ya da alt sınıfından) mı |
| `class HouseError(ValueError): ...` | kendi istisnan, var olandan türeyerek |

## İşleç aşırı yükleme

| Metot | İşleç |
|---|---|
| `__add__(self, other)` | `a + b` |
| `__sub__(self, other)` | `a - b` |
| `__eq__(self, other)` | `a == b` |
| `__lt__(self, other)` | `a < b` |
| `__str__(self)` | `str(a)`, `print(a)` |

## Yerleşik türler

`int`, `str`, `list`, `dict` de sınıf: `type(50)` → `<class 'int'>`.
`"hi".lower()` bir `str` nesnesinin metodu.
