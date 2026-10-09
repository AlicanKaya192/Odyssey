# pickle ve Serileştirme

Bellekteki bir nesneyi dosyaya yazılabilir ya da ağdan gönderilebilir bir
bayt dizisine çevirmeye **serileştirme** (serialization), geri çevirmeye
**ters serileştirme** denir. Python patikasının JSON bölümünde bunun bir
yolunu gördün: `json`. Bu bölüm Python'un kendi biçimini anlatıyor:
**`pickle`**. JSON'un taşıyamadığı demeti, kümeyi, tarihi, kendi sınıflarını
olduğu gibi saklıyor; ama bunun bir bedeli var ve o bedel bir **güvenlik**
konusu.

## dumps ve loads

```python
import json
import pickle
from datetime import date

data = {"name": "ada", "tags": {"math", "code"}, "point": (3, 4),
        "born": date(1815, 12, 10)}
blob = pickle.dumps(data)
back = pickle.loads(blob)
print(type(blob).__name__, back == data)
print(type(back["point"]).__name__, type(back["born"]).__name__)
try:
    json.dumps(data)
except TypeError as error:
    print("json:", error)
```

```text
bytes True
tuple date
json: Object of type set is not JSON serializable
```

- **`pickle.dumps(nesne)`** nesneyi `bytes`'a çevirir, **`pickle.loads(baytlar)`**
  geri kurar. Adlar `json` ile aynı: `s` metin değil, burada "bellekteki
  baytlar" demek.
- Geri gelen nesne **eşit** ve türler korunmuş: demet demet, tarih tarih,
  küme küme kaldı. JSON aynı sözlükte kümeyi görünce durdu.
- Sonuç ikili veri (binary); bir metin düzenleyicide okunmaz, Python
  dışındaki dillerde de açılmaz.

## Dosyaya yazmak: dump ve load

```python
import pickle
from pathlib import Path

scores = {"ada": [90, 85], "alan": [75]}
path = Path("scores.pkl")
with path.open("wb") as file:
    pickle.dump(scores, file)
with path.open("rb") as file:
    print(pickle.load(file))
try:
    with path.open("w") as file:
        pickle.dump(scores, file)
except TypeError as error:
    print("TypeError:", error)
```

```text
{'ada': [90, 85], 'alan': [75]}
TypeError: write() argument must be str, not bytes
```

- **`pickle.dump(nesne, dosya)`** / **`pickle.load(dosya)`**: `s`'siz hâller
  doğrudan dosyayla çalışır.
- Dosya **ikili kipte** açılır: yazarken `"wb"`, okurken `"rb"`. Metin kipinde
  (`"w"`) açılan dosyaya bayt yazılamaz; en sık yapılan hata budur.
- Uzantı serbest; `.pkl` ya da `.pickle` yaygın.

## Kendi nesnelerin

```python
import pickle


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


p = Point(1, 2)
back = pickle.loads(pickle.dumps([p, p]))
print(back, back[0] is back[1])
node = {"name": "root"}
node["self"] = node
copy = pickle.loads(pickle.dumps(node))
print(copy["self"] is copy)
blob = pickle.dumps(Point(3, 4))
del Point
try:
    pickle.loads(blob)
except AttributeError as error:
    print("AttributeError:", error)
```

```text
[Point(1, 2), Point(1, 2)] True
True
AttributeError: module '__main__' has no attribute 'Point'
```

- Sınıf örnekleri de saklanır: pickle nesnenin **özelliklerini** ve
  **sınıfının adını** (`__main__.Point`) yazar.
- Aynı nesneye iki başvuru geri gelince de **tek nesne** (`is` → `True`);
  kendini gösteren bir sözlük gibi döngüler de sorun değil.
- **Sınıfın kodu dosyada yok.** Yüklerken pickle sınıfı adıyla arar;
  bulamazsa (sınıf silindi, adı değişti, başka programda tanımlı değil)
  yükleme düşer. Uzun süre saklanan pickle dosyaları bu yüzden kırılgandır:
  sınıfın adını değiştirmek eski dosyaları açılmaz yapar.

## Saklanmayacak parçalar

Bazı nesneler serileştirilemez: kilitler, açık dosyalar, veritabanı
bağlantıları. Bunlardan birini tutan bir sınıf da saklanamaz.

```python
import pickle
import threading


class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def add(self):
        with self.lock:
            self.count += 1

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["lock"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()


try:
    pickle.dumps(threading.Lock())
except TypeError as error:
    print("TypeError:", error)
c = Counter()
c.add()
c.add()
back = pickle.loads(pickle.dumps(c))
back.add()
print(back.count, type(back.lock).__name__)
```

```text
TypeError: cannot pickle '_thread.lock' object
3 lock
```

- **`__getstate__`** saklanacak durumu döndürür: özelliklerin bir kopyası,
  kilit çıkarılmış.
- **`__setstate__`** yüklenirken çağrılır: durumu geri koyar ve kilidi
  **yeniden kurar**. Yüklenen sayaç çalışmaya devam ediyor.
- Aynı kalıp bağlantılar ve önbellekler için de geçerli: saklama, yükleyince
  yeniden kur.

## Güvenlik: pickle.loads kod çalıştırır

```python
import pickle


class Trap:
    def __reduce__(self):
        return (print, ("this ran while loading!",))


blob = pickle.dumps(Trap())
print(len(blob) > 0)
pickle.loads(blob)
```

```text
True
this ran while loading!
```

- **`__reduce__`** bir nesnenin "nasıl yeniden kurulacağını" söyler: bir
  fonksiyon ve argümanları. pickle yüklerken o fonksiyonu **çağırır**.
- Burada zararsız `print` çağrıldı; kötü niyetli biri aynı yolla dosya
  silen ya da program indiren bir çağrı koyabilir. Yalnızca `loads` yetiyor,
  nesneyi kullanmana bile gerek yok.
- **Kural: güvenmediğin kaynaktan gelen pickle verisini asla yükleme**
  (internetten indirilen dosya, kullanıcının yüklediği veri, ağdan gelen
  mesaj). Dışarıyla veri alışverişi için JSON kullanılır; JSON yalnızca veri
  taşır, kod çalıştıramaz.

## shelve: sözlük gibi kalıcı depo

```python
import shelve

with shelve.open("cache") as db:
    db["ada"] = {"score": 90}
    db["alan"] = {"score": 75}
with shelve.open("cache") as db:
    print(sorted(db), db["ada"]["score"])
    db["ada"]["score"] = 100
with shelve.open("cache") as db:
    print(db["ada"]["score"])
    record = db["ada"]
    record["score"] = 100
    db["ada"] = record
with shelve.open("cache") as db:
    print(db["ada"]["score"])
```

```text
['ada', 'alan'] 90
90
100
```

- **`shelve`** diskte duran bir sözlük: anahtarlar metin, değerler pickle ile
  saklanan herhangi bir nesne. Her değeri ayrı ayrı okuyup yazdığı için
  bütün veriyi belleğe almaz.
- **Tuzak:** `db["ada"]["score"] = 100` kayda **yazılmadı** (yine 90).
  `db["ada"]` diskten okunan bir **kopya** veriyor; kopyayı değiştirmek
  diske dokunmuyor. Doğrusu: al, değiştir, **geri ata** (`db["ada"] =
  record`). (`shelve.open(..., writeback=True)` de çözüyor ama okunan her
  şeyi bellekte tutuyor.)
- shelve de pickle kullanır: aynı güvenlik kuralı geçerli.

## Hangisi ne zaman?

| | `json` | `pickle` |
|---|---|---|
| Okunabilir | metin, gözle okunur | ikili |
| Diller | her dil | yalnızca Python |
| Türler | sözlük, liste, metin, sayı, `bool`, `None` | neredeyse her Python nesnesi |
| Güvenlik | yalnızca veri | yüklerken kod çalıştırabilir |
| Kullanım | dosya biçimi, API, ayarlar | Python içi geçici önbellek, süreçler arası |

Python'un kendisi de pickle'ı kullanıyor: `multiprocessing` süreçlere
gönderdiği nesneleri ve sonuçları pickle ile taşıyor (Büyük Veri
patikasındaki süreç havuzu), `copy.deepcopy` de aynı `__reduce__` düzenini
kullanıyor.

## Özet

- `pickle.dumps` / `loads` bellekte, `dump` / `load` dosyayla; dosya `"wb"` /
  `"rb"`.
- Türler ve aynı nesneye başvurular korunur; sınıf adıyla aranır, kodu
  saklanmaz.
- Saklanamayan parçalar için `__getstate__` / `__setstate__`.
- **Güvenilmeyen pickle verisi yüklenmez**: `loads` kod çalıştırabilir.
- `shelve` diskte sözlük; değeri değiştirince geri ata.
