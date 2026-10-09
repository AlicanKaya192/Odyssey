# dataclasses

Python patikasının OOP bölümünde sınıf yazdın: `__init__` içinde her alanı
`self.x = x` diye tek tek atadın. Çoğu sınıf aslında **veri taşır**: bir
ürün, bir kullanıcı, bir koordinat. Bu sınıflar için her seferinde aynı
`__init__`'i, yazdırıldığında okunur görünmesi için `__repr__`'ı,
karşılaştırma için `__eq__`'yu yazmak gerekir. **`dataclasses`** bunları alan
listesinden kendisi üretir.

## @dataclass

```python
from dataclasses import dataclass


class PlainPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


print("object at" in repr(PlainPoint(1, 2)), PlainPoint(1, 2) == PlainPoint(1, 2))


@dataclass
class Point:
    x: float
    y: float


p = Point(1, 2)
print(p, p == Point(1, 2), p.x + p.y)
```

```text
True False
Point(x=1, y=2) True 3
```

- Düz sınıfın yazdırılışı `<... object at 0x...>` (hiçbir şey söylemiyor) ve
  aynı değerli iki nesne **eşit değil** (`==` kimliğe bakıyor).
- **`@dataclass`** sınıfın tür belirtimli alanlarını okuyup `__init__`,
  `__repr__` ve `__eq__`'yu kendisi yazdı: `Point(x=1, y=2)` okunur, aynı
  değerliler eşit.
- Alanlar tür belirtimiyle yazılır; belirtim burada da denetlenmez
  (`Point(1, 2)` tam sayıyla kuruldu).

## Varsayılanlar ve field

```python
from dataclasses import dataclass, field


@dataclass
class Cart:
    owner: str
    items: list[str] = field(default_factory=list)
    discount: float = 0.0


a = Cart("ada")
b = Cart("alan", discount=0.1)
a.items.append("pen")
print(a)
print(b)
try:
    @dataclass
    class Bad:
        items: list = []
except ValueError as error:
    print("ValueError:", str(error).split(":")[0])
```

```text
Cart(owner='ada', items=['pen'], discount=0.0)
Cart(owner='alan', items=[], discount=0.1)
ValueError: mutable default <class 'list'> for field items is not allowed
```

- Varsayılanı olan alanlar varsayılansızlardan **sonra** yazılır.
- Liste, sözlük gibi **değiştirilebilir** varsayılan `= []` ile yazılamaz:
  bütün nesneler aynı listeyi paylaşırdı. `dataclass` buna izin vermiyor
  (`ValueError`) ve mesajın devamında çözümü söylüyor: **`field(default_factory=list)`**
  her nesne için yeni bir liste kurar. `a`'ya eklenen `pen`, `b`'ye geçmedi.

## frozen ve order

```python
from dataclasses import FrozenInstanceError, dataclass


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int = 0


v = Version(1, 2)
try:
    v.major = 3
except FrozenInstanceError as error:
    print("FrozenInstanceError:", error)
versions = sorted([Version(1, 10), Version(1, 2), Version(0, 9)])
print([f"{x.major}.{x.minor}" for x in versions])
print(len({v, Version(1, 2), Version(2)}), Version(2) > v)
```

```text
FrozenInstanceError: cannot assign to field 'major'
['0.9', '1.2', '1.10']
2 True
```

- **`frozen=True`** nesneyi değişmez yapar: alan atanamaz. Değişmez nesne
  **küme elemanı ve sözlük anahtarı** olabilir (hash'i var): üç sürümden
  ikisi aynıydı, kümede iki kaldı.
- **`order=True`** `<`, `>` karşılaştırmalarını alan sırasıyla (önce
  `major`, sonra `minor`) üretir; `sorted` ve `max` çalışır. Alanların
  yazılış sırası karşılaştırma sırasıdır.

## __post_init__, asdict, replace

```python
from dataclasses import asdict, dataclass, field, replace


@dataclass
class Rect:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self):
        if self.width < 0 or self.height < 0:
            raise ValueError("negative size")
        self.area = self.width * self.height


r = Rect(3, 4)
print(r, asdict(r))
print(replace(r, width=10))
try:
    Rect(-1, 2)
except ValueError as error:
    print("ValueError:", error)
```

```text
Rect(width=3, height=4, area=12) {'width': 3, 'height': 4, 'area': 12}
Rect(width=10, height=4, area=40)
ValueError: negative size
```

- **`__post_init__`** üretilen `__init__`'ten hemen sonra çalışır:
  **doğrulama** ve hesaplanan alanlar için.
- **`field(init=False)`** alan `__init__`'te istenmez; `__post_init__`
  doldurur.
- **`asdict`** nesneyi sözlüğe çevirir (JSON'a yazmadan önce);
  **`replace`** bir alanı değişmiş **yeni** nesne üretir (`frozen`
  nesnelerde değişiklik böyle yapılır). Yeni nesne yeniden `__post_init__`'ten
  geçti: alan 40 oldu.

## slots ve kw_only

```python
from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class User:
    name: str
    admin: bool = False


u = User(name="ada")
print(u)
try:
    User("ada")
except TypeError as error:
    print("TypeError:", error)
try:
    u.email = "ada@example.com"
except AttributeError as error:
    print(type(error).__name__)
```

```text
User(name='ada', admin=False)
TypeError: User.__init__() takes 1 positional argument but 2 were given
AttributeError
```

- **`kw_only=True`**: alanlar yalnızca adıyla verilir (`User(name="ada")`).
  Çok alanlı kayıtlarda sırayı karıştırmayı önler.
- **`slots=True`**: nesne yalnızca tanımlı alanları taşır. Yanlış yazılan bir
  ad (`u.emial = ...`) sessizce yeni alan açmak yerine hata verir; nesne de
  daha az bellek kullanır.

## JSON'a gidip gelmek

```python
import json
from dataclasses import asdict, dataclass


@dataclass
class User:
    name: str
    age: int
    tags: list[str]


users = [User("ada", 36, ["math"]), User("alan", 41, [])]
text = json.dumps([asdict(u) for u in users])
print(json.dumps(asdict(users[0])))
loaded = [User(**d) for d in json.loads(text)]
print(loaded == users, loaded[1])
```

```text
{"name": "ada", "age": 36, "tags": ["math"]}
True User(name='alan', age=41, tags=[])
```

Yazarken `asdict`, okurken `User(**sözlük)`: `**` sözlüğün anahtarlarını
adlı argüman olarak verir. Gelen JSON'da fazla ya da eksik anahtar varsa
`TypeError` olur; dışarıdan gelen veride bunu yakalamak gerekir.

## Özet

- `@dataclass`: alanlardan `__init__`, `__repr__`, `__eq__`.
- Değiştirilebilir varsayılan `field(default_factory=list)`.
- `frozen=True` değişmez ve hash'lenebilir, `order=True` sıralanabilir.
- `__post_init__` doğrulama ve hesaplanan alan; `field(init=False)`.
- `asdict` sözlüğe, `replace` değişmiş kopya, `Sınıf(**d)` geri.
- `slots=True` yanlış adı yakalar, `kw_only=True` adla verdirir.
