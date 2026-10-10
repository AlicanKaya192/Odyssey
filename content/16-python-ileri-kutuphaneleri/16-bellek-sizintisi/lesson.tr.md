# Bellek Sızıntısı

Bir sunucu açılışta 200 MB bellek kullanıyor; bir gün sonra 2 GB, bir hafta
sonra makine belleği bitiyor ve program çöküyor. Bu bir **bellek sızıntısı**
(memory leak): artık işe yaramayan veri bellekte kalmaya devam ediyor ve
birikiyor. Python belleği kendisi yönetir, `free` yazmazsın; o yüzden
"Python'da sızıntı olmaz" sanılır. Olur, ama sebebi farklıdır: **bir yerde
hâlâ duran bir başvuru** (referans). Bu bölüm Python'un belleği nasıl
boşalttığını, sızıntının tipik kaynaklarını, nasıl bulunacağını ve nasıl
önleneceğini anlatıyor.

## Başvuru sayımı: nesne ne zaman silinir?

```python
import sys
import weakref


class Node:
    def __init__(self, name):
        self.name = name
        self.other = None


a = Node("a")
weakref.finalize(a, print, "freed a")
print(sys.getrefcount(a))
b = a
print(sys.getrefcount(a))
del b
del a
print("after del")
```

```text
2
3
freed a
after del
```

- Python her nesne için **kaç yerden gösterildiğini** sayar (başvuru sayısı,
  reference count). `sys.getrefcount(a)` bunu verir; çağrının kendisi de
  geçici bir başvuru eklediği için bir fazla görünür.
- `b = a` yeni bir **ad** açar, yeni nesne değil: sayı 3 oldu.
- Son başvuru da gidince (`del a`) sayı sıfıra düşer ve nesne **hemen**
  silinir: "freed a", "after del"den önce yazıldı.
- **`weakref.finalize(nesne, fonksiyon, ...)`** nesne silinince çağrılacak bir
  fonksiyon kaydeder; nesneyi canlı tutmaz. Bu bölümde "silindi mi?"
  sorusunu bununla görüyoruz.

## Döngüler ve çöp toplayıcı (gc)

```python
import gc
import weakref


class Node:
    def __init__(self, name):
        self.name = name
        self.other = None


gc.disable()
x = Node("x")
y = Node("y")
x.other = y
y.other = x
weakref.finalize(x, print, "freed x")
weakref.finalize(y, print, "freed y")
del x, y
print("names deleted")
found = gc.collect()
print(found >= 2)
gc.enable()
```

```text
names deleted
freed x
freed y
True
```

- `x` `y`'yi, `y` `x`'i gösteriyor: bir **döngü** (reference cycle). Adlar
  silinse de her birinin sayısı 1'de kalır (birbirlerini gösteriyorlar);
  başvuru sayımı onları silemez.
- Python'un ikinci mekanizması **döngüsel çöp toplayıcı** (`gc`): ara sıra
  nesneleri tarayıp dışarıdan ulaşılamayan döngüleri bulur ve siler. Burada
  bunu görmek için otomatik toplamayı kapattık (`gc.disable()`) ve
  `gc.collect()` ile elle çalıştırdık.
- Toplayıcı normalde kendiliğinden çalışır; yani döngüler **sonunda**
  silinir. Ama ne zaman çalışacağı belli değildir ve büyük döngüler belleği o
  ana kadar tutar. `gc.disable()` gerçek programda yazılmaz.

## Sızıntı 1: sınırsız büyüyen önbellek

```python
import tracemalloc
from functools import lru_cache

tracemalloc.start()
_cache = {}


def handle(request_id):
    result = f"report {request_id} " * 50
    _cache[request_id] = result
    return len(result)


before = tracemalloc.get_traced_memory()[0]
for i in range(10_000):
    handle(i)
grown = (tracemalloc.get_traced_memory()[0] - before) / 1024


@lru_cache(maxsize=100)
def handle_bounded(request_id):
    return f"report {request_id} " * 50


before = tracemalloc.get_traced_memory()[0]
for i in range(10_000):
    handle_bounded(i)
bounded = (tracemalloc.get_traced_memory()[0] - before) / 1024
print(len(_cache), round(grown))
print(handle_bounded.cache_info().currsize, round(bounded))
```

```text
10000 6798
100 80
```

- **En sık sızıntı budur.** "Bir daha lazım olur" diye her sonucu modül
  düzeyindeki bir sözlüğe koymak: sözlük asla küçülmez. Her istek için yeni
  bir anahtar geliyorsa (kullanıcı kimliği, zaman damgası) program açık
  kaldıkça büyür. 10 000 istekte yaklaşık 6,8 MB; bir milyon istekte yüzlerce
  MB.
- **`tracemalloc`** Python'un ayırdığı belleği izler:
  `get_traced_memory()` → `(şu an, tepe)` bayt.
- Çözüm: önbelleğe **sınır** koymak. **`lru_cache(maxsize=100)`** en son
  kullanılan 100 sonucu tutar, en eskisini atar (functools bölümü). Bellek
  80 KB'ta kaldı.
- Aynı sorun modül düzeyindeki listede (`log_lines.append(...)`), sınıf
  özelliğinde (bütün örneklerin paylaştığı liste) ve `lru_cache(maxsize=None)`
  ile de olur.

## Sızıntı 2: unutulan dinleyiciler

```python
import gc
import weakref


class Bus:
    def __init__(self):
        self.listeners = []

    def subscribe(self, callback):
        self.listeners.append(callback)


class WeakBus:
    def __init__(self):
        self.listeners = []

    def subscribe(self, callback):
        self.listeners.append(weakref.WeakMethod(callback))

    def emit(self, event):
        alive = []
        for ref in self.listeners:
            callback = ref()
            if callback is not None:
                callback(event)
                alive.append(ref)
        self.listeners = alive


class Widget:
    def __init__(self, bus, name):
        weakref.finalize(self, print, "freed", name)
        bus.subscribe(self.on_event)

    def on_event(self, event):
        pass


bus = Bus()
w = Widget(bus, "w1")
del w
gc.collect()
print("strong listeners:", len(bus.listeners))
weak_bus = WeakBus()
w = Widget(weak_bus, "w2")
del w
weak_bus.emit("tick")
print("weak listeners:", len(weak_bus.listeners))
```

```text
strong listeners: 1
freed w2
weak listeners: 0
freed w1
```

- `Widget` kendini olay yoluna (bus) kaydediyor: `bus.listeners` artık
  `self.on_event`'i, o da `self`'i gösteriyor. Widget'ı silmek yetmiyor;
  `gc.collect()` de silemiyor, çünkü bu bir döngü değil, **ulaşılabilir**
  bir başvuru. "w1" ancak program **kapanırken** silindi (son satır).
- Arayüz pencereleri, eklentiler, olay dinleyicileri, geri çağırmalar
  (callback) sık sızar: pencere kapanır ama kaydı durur.
- Çözüm 1: kapanırken **aboneliği bırak** (`unsubscribe`).
- Çözüm 2: **zayıf başvuru** (weak reference). `weakref.WeakMethod` metodu
  gösterir ama nesneyi canlı tutmaz; nesne gidince `ref()` `None` döner ve
  liste temizlenir. Düz nesneler için `weakref.ref`, `WeakSet`,
  `WeakValueDictionary`.
- Çıktıda: "w2" `del w` anında silindi; olay gönderilince ölü kayıt da
  listeden atıldı (`0`).

## Sızıntıyı bulmak: tracemalloc karşılaştırması

```python
import tracemalloc
from pathlib import Path

tracemalloc.start()
first = tracemalloc.take_snapshot()
kept = [bytearray(1000) for _ in range(2000)]
second = tracemalloc.take_snapshot()
top = second.compare_to(first, "lineno")[0]
frame = top.traceback[0]
print(Path(frame.filename).name, frame.lineno)
print(top.size_diff // 1024 > 1900)
tracemalloc.stop()
```

```text
main.py 6
True
```

- **`take_snapshot()`** o anki bütün ayırmaların fotoğrafını çeker.
  İki fotoğrafı **`compare_to(önceki, "lineno")`** ile karşılaştırınca
  bellek artışı **satır satır**, büyükten küçüğe sıralanır.
- İlk sıradaki satır, belleği tutan kodun yeri: 6. satır (listenin
  kurulduğu satır), yaklaşık 2 MB.
- Uzun çalışan bir programda: belirli aralıklarla fotoğraf al, ilk sıralarda
  sürekli büyüyen satırı ara. (Notlarda tam örnek var.)
- `tracemalloc` **Python'a bildirilen** ayırmaları görür. Bazı kütüphanelerin
  C tarafında ayırdığı bellek görünmeyebilir; pandas'ın Arrow tabanlı
  sütunları böyledir (Büyük Veri patikasında ölçülmüştü).

## Öteki kaynaklar

| Kaynak | Ne oluyor | Önlem |
|---|---|---|
| Kapatılmayan dosya / bağlantı | işletim sistemi kaynağı açık kalıyor | `with` |
| `__del__` ile temizlik | ne zaman çalışacağı belli değil | `with` ve bağlam yöneticisi (contextlib bölümü) |
| Kapanış (closure) | iç fonksiyon büyük bir nesneyi yakalıyor | yalnızca gerekeni yakala |
| Saklanan hata | hata nesnesi `__traceback__` ile bütün çerçeveleri tutar | hatayı uzun süre saklama, yalnızca metnini sakla |
| Bitmeyen iş parçacığı | kendi verisiyle yaşamaya devam ediyor | durdurma işareti, `join` |
| Jupyter | her çıktı `Out[n]` ve `_` değişkenlerinde kalıyor | `del` + `gc.collect()`, çekirdeği yeniden başlat |

`__del__` hakkında: Python 3.4'ten beri `__del__`'i olan nesneler döngüde de
toplanıyor; asıl sorun zamanlamanın belirsiz olması. Dosya, kilit, bağlantı
gibi kaynakların bırakılması `with` ile garanti edilir.

## Özet

- Python başvuru sayısı sıfıra düşen nesneyi hemen siler; döngüleri `gc`
  ara sıra toplar.
- Sızıntı = işe yaramayan ama hâlâ **ulaşılabilir** veri: büyüyen önbellek,
  unutulan dinleyici, saklanan hata.
- Önbelleğe sınır (`lru_cache(maxsize=...)`), dinleyiciye zayıf başvuru ya
  da abonelikten çıkış.
- `tracemalloc`: `get_traced_memory`, `take_snapshot`, `compare_to`.
- `weakref.finalize` ile bir nesnenin gerçekten silindiğini doğrula.
