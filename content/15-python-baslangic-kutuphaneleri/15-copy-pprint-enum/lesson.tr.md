# copy, pprint ve enum

Bu bölümde üç küçük ama her projede işe yarayan modül var. **`copy`**:
iç içe bir yapıyı (listeli sözlük gibi) kopyalarken içteki parçaların
**paylaşılıp paylaşılmadığını** kontrol etmek. **`pprint`**: büyük ve iç içe
veriyi okunur biçimde yazdırmak. **`enum`**: `"paid"`, `"shipped"` gibi sabit
seçenekleri yazım hatasına açık metinler yerine adlı değerlerle tutmak.

## Atama, sığ kopya, derin kopya

```python
import copy

original = {"name": "Ada", "tags": ["math", "code"]}
alias = original
shallow = copy.copy(original)
deep = copy.deepcopy(original)
original["name"] = "Grace"
original["tags"].append("ships")
print(alias["name"], shallow["name"], deep["name"])
print(shallow["tags"], deep["tags"])
print(alias is original, shallow is original, shallow["tags"] is original["tags"])
```

```text
Grace Ada Ada
['math', 'code', 'ships'] ['math', 'code']
True False True
```

- **Atama** (`alias = original`) kopya değildir: iki ad **aynı** sözlüğü
  gösterir. Birinden yapılan değişiklik ötekinde görünür (`Grace`).
- **Sığ kopya** (`copy.copy`, `dict(d)`, `list(x)`, `x[:]`, `d.copy()`) dış
  kabı yeniden kurar ama **içteki nesneleri paylaşır**: ad değişikliği
  kopyaya geçmedi (`Ada`), ama içteki listeye eklenen `ships` sığ kopyada da
  görünüyor. İkisinin `tags`'i aynı liste (`is` → `True`).
- **Derin kopya** (`copy.deepcopy`) iç içe her şeyi yeniden kurar: hiçbir
  değişiklik ona geçmedi.

Bir fonksiyon aldığı iç içe veriyi değiştirecekse ve çağıranın verisi
bozulmasın isteniyorsa `deepcopy` gerekir. Derin kopya büyük veride yavaştır
ve bellek ister; gerçekten iç içe değişiklik yapılacaksa kullanılır.

## Sık hata: [[0] * 3] * 3

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 1
print(grid)
```

```text
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
[[1, 0, 0], [0, 0, 0], [0, 0, 0]]
```

Listeyi `* 3` ile çoğaltmak içteki listeyi **kopyalamaz**, aynı listeye üç
kez işaret eder: bir hücreyi değiştirince üç satır birden değişti. Her satır
için **yeni** liste kuran kavrama doğru sonucu verir. Bu, sığ kopyanın
gizli bir hâli.

## pprint: okunur yazdırmak

```python
from pprint import pformat, pprint

data = {"version": "1.0.0", "name": "Odyssey",
        "tracks": [{"id": "python", "sections": 19, "tags": ["basics", "oop"]},
                   {"id": "sql", "sections": 20, "tags": ["joins"]}]}
print(len(repr(data)))
pprint(data, width=60)
pprint(data, depth=1)
pprint(data, depth=1, sort_dicts=False)
print(repr(pformat([1, 2, 3])))
```

```text
162
{'name': 'Odyssey',
 'tracks': [{'id': 'python',
             'sections': 19,
             'tags': ['basics', 'oop']},
            {'id': 'sql',
             'sections': 20,
             'tags': ['joins']}],
 'version': '1.0.0'}
{'name': 'Odyssey', 'tracks': [...], 'version': '1.0.0'}
{'version': '1.0.0', 'name': 'Odyssey', 'tracks': [...]}
'[1, 2, 3]'
```

- Düz `print(data)` tüm yapıyı tek satıra döker: burada
  162 karakterlik bir satır, okunmaz.
- **`pprint`** (pretty print) satırlara böler ve iç içe düzeyleri hizalar;
  `width` satır genişliği.
- **`depth=1`** yalnızca ilk düzeyi gösterir, daha derindekini `[...]` yapar:
  büyük bir JSON yanıtının ne içerdiğine hızla bakmak için.
- `pprint` sözlük anahtarlarını **varsayılan olarak sıralar**; özgün sırayı
  görmek için `sort_dicts=False`.
- **`pformat`** aynı metni ekrana yazmadan döndürür (kayıt dosyasına
  yazmak için).

## enum: adlı sabitler

```python
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"


order = Status.PAID
print(order, order.name, order.value)
print(Status("shipped"), Status["PENDING"])
print(order == Status.PAID, order == "paid")
print([s.name for s in Status])
try:
    Status("lost")
except ValueError as error:
    print("ValueError:", error)
```

```text
Status.PAID PAID paid
Status.SHIPPED Status.PENDING
True False
['PENDING', 'PAID', 'SHIPPED']
ValueError: 'lost' is not a valid Status
```

- Bir **`Enum`** sınıfı, bir şeyin alabileceği **sabit seçenekleri** listeler:
  sipariş durumu, kullanıcı rolü, renk.
- Her üyenin `name`'i (`PAID`) ve `value`'su (`"paid"`) var. Dışarıdan gelen
  değerden üyeye `Status("shipped")`, addan `Status["PENDING"]`.
- Üye düz metne **eşit değildir** (`order == "paid"` → `False`): karşılaştırma
  hep üyelerle yapılır.
- Sınıf dolaşılabilir; geçersiz bir değer `ValueError` verir. Dosyadan ya da
  API'den gelen bir durumu doğrulamak kendiliğinden olmuş olur.

## IntEnum ve Flag

```python
from enum import Flag, IntEnum, auto


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


print(Priority.HIGH > Priority.LOW, Priority.MEDIUM + 1)
print(sorted([Priority.HIGH, Priority.LOW, Priority.MEDIUM]))


class Perm(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


p = Perm.READ | Perm.WRITE
print(p, Perm.WRITE in p, Perm.EXECUTE in p)
print(Perm.READ.value, Perm.WRITE.value, Perm.EXECUTE.value)
```

```text
True 3
[<Priority.LOW: 1>, <Priority.MEDIUM: 2>, <Priority.HIGH: 3>]
Perm.READ|WRITE True False
1 2 4
```

- **`IntEnum`** üyeleri aynı zamanda tam sayıdır: büyüklük karşılaştırılır,
  sıralanır, hesaba girer. Öncelik, seviye gibi sıralı seçenekler için.
- **`Flag`** birleştirilebilen seçenekler: bir dosya izni hem okuma hem yazma
  olabilir. `|` ile birleştirilir, `in` ile sorulur.
- **`auto()`** değeri kendisi verir; `Flag`'de 1, 2, 4... (her biri ayrı bir
  bit), böylece birleşimler karışmaz.

## Özet

- Atama kopya değil; `copy.copy` sığ (içi paylaşılır), `copy.deepcopy` derin.
- `[[0] * 3] * 3` aynı listeyi üç kez gösterir; kavrama kullan.
- `pprint(veri, width=, depth=, sort_dicts=)`, `pformat`.
- `Enum`: `name`, `value`, `Status("değer")`, `Status["AD"]`; metne eşit
  değil.
- `IntEnum` sıralanabilir, `Flag` `|` ile birleşir; `auto()`.
