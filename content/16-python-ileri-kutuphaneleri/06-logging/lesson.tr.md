# logging

Küçük betikte ne olduğunu `print` ile görürsün. Büyüyen bir programda bu
yetmez: bazı mesajlar yalnızca hata ayıklarken gerekir, bazıları her zaman;
bazıları ekrana, bazıları dosyaya gitmeli; her mesajın zamanı ve hangi
modülden geldiği bilinmeli. **`logging`** bunun standart aracıdır: kayıtları
**düzeylere** ayırır, **adlı kaydedicilerle** (logger) kaynağını belirtir ve
**işleyicilerle** (handler) istenen yere yazar.

## Düzeyler ve basicConfig

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s")
logging.debug("details only a developer needs")
logging.info("server started on port %d", 8000)
logging.warning("disk %d%% full", 91)
logging.error("could not save %s", "report.csv")
```

```text
INFO root: server started on port 8000
WARNING root: disk 91% full
ERROR root: could not save report.csv
```

- Beş düzey var: `DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`.
  `level=logging.INFO` verilince `INFO` ve üstü yazıldı, `DEBUG` atlandı.
  Hata ayıklarken düzeyi `DEBUG`'a indirmek yeter; kodda `print` silmeye
  gerek kalmaz.
- **`basicConfig`** en basit kurulumu tek satırda yapar: nereye (`stream`,
  varsayılan hata akışı stderr), hangi düzeyden itibaren, hangi biçimde.
- Biçimdeki `%(levelname)s`, `%(name)s`, `%(message)s` kaydın alanları;
  gerçek programlarda başa `%(asctime)s` (zaman) da eklenir.
- Mesajdaki değerler **ayrı argüman** verilir (`"port %d", 8000`); neden
  önemli olduğu sık hatalar kısmında.

## Adlı kaydediciler

```python
import logging
import sys

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(name)s [%(levelname)s] %(message)s"))
root = logging.getLogger()
root.addHandler(handler)
root.setLevel(logging.WARNING)

db = logging.getLogger("shop.db")
web = logging.getLogger("shop.web")
logging.getLogger("shop.db").setLevel(logging.DEBUG)
db.debug("query took 3 ms")
web.info("GET /home")
web.warning("slow response")
print(db.parent.name, web.getEffectiveLevel(), db.getEffectiveLevel())
```

```text
shop.db [DEBUG] query took 3 ms
shop.web [WARNING] slow response
root 30 10
```

- **`logging.getLogger(ad)`** adlı bir kaydedici verir; aynı adla her
  çağrıda **aynı** nesne gelir. Modüllerde `log = logging.getLogger(__name__)`
  yazılır: kaydın hangi modülden geldiği adından okunur.
- Adlar noktalarla bir **ağaç** kurar: `shop.db`'nin üstü `shop` olurdu;
  burada `shop` adında bir kaydedici hiç istenmediği için üstü doğrudan kök
  (`root`). Kendi düzeyi olmayan kaydedici üstündekinin düzeyini
  kullanır: `shop.web` köke uydu (`30` = `WARNING`), `INFO`'su yazılmadı;
  `shop.db`'ye `DEBUG` (`10`) verildi, yalnızca o konuşkan oldu.
- Kayıtlar ağaçta yukarı **yayılır** ve kökteki işleyici hepsini yazdı.

## İşleyiciler: ekran ve dosya

```python
import logging
import sys
from pathlib import Path

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
screen = logging.StreamHandler(sys.stdout)
screen.setLevel(logging.WARNING)
screen.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
file = logging.FileHandler("app.log", encoding="utf-8")
file.setFormatter(logging.Formatter("%(levelname)s %(funcName)s: %(message)s"))
log.addHandler(screen)
log.addHandler(file)


def load():
    log.debug("reading config")
    log.warning("config missing, using defaults")


load()
file.close()
print(Path("app.log").read_text(encoding="utf-8"))
```

```text
WARNING: config missing, using defaults
DEBUG load: reading config
WARNING load: config missing, using defaults
```

Bir kaydedicinin birden çok **işleyicisi** olabilir, her birinin kendi
düzeyi ve biçimi var: ekrana yalnızca uyarılar (ilk satır), dosyaya her şey,
ayrıntılı biçimde (`%(funcName)s` kaydı yazan fonksiyon). Programın
kullanıcısı ekranı temiz görür; sorun çıkınca dosyada ayrıntı vardır.
Uzun süre çalışan programlarda dosya büyümesin diye
`logging.handlers.RotatingFileHandler` belli boyutta yeni dosyaya geçer.

## Hata kaydetmek: exception

```python
import io
import logging

buffer = io.StringIO()
handler = logging.StreamHandler(buffer)
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
log = logging.getLogger("calc")
log.addHandler(handler)


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        log.exception("divide failed for a=%s b=%s", a, b)
        return None


print(divide(6, 0))
lines = buffer.getvalue().splitlines()
print(lines[0])
print(lines[1])
print(lines[-1])
```

```text
None
ERROR: divide failed for a=6 b=0
Traceback (most recent call last):
ZeroDivisionError: division by zero
```

**`log.exception(...)`** `except` bloğunun içinde çağrılır: mesajı `ERROR`
düzeyinde yazar ve **hata izini** (traceback) ekler. Aradaki satırlarda
hatanın hangi dosyada, hangi satırda çıktığı var (burada yazdırmadık).
Hatayı yakalayıp sessizce `None` döndürmek yerine en azından kaydetmek, bir
hafta sonra "neden boş geldi" sorusunun cevabıdır.

## Sık hatalar

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
log = logging.getLogger("demo")
calls = 0


class Expensive:
    def __str__(self):
        global calls
        calls += 1
        return "expensive"


log.debug("value: %s", Expensive())
log.debug(f"value: {Expensive()}")
print(calls)
logging.basicConfig(level=logging.DEBUG)
log.debug("still hidden")
print(logging.getLogger().level == logging.INFO)
```

```text
1
True
```

- **f-string ile kayıt:** `DEBUG` kapalıyken bile f-string metni **önceden**
  kurulur: `__str__` bir kez çağrıldı. `"%s", değer` biçiminde metin ancak
  kayıt gerçekten yazılacaksa kurulur. Sık çağrılan yerlerde fark büyür.
- **İkinci `basicConfig` hiçbir şey yapmaz:** kök kaydedicinin işleyicisi
  zaten varsa yok sayılır (düzey `INFO` kaldı). Kurulumu programın en
  başında bir kez yap; değiştirmek gerekirse `force=True`.
- Kütüphane yazıyorsan `basicConfig` çağırma; yalnızca
  `getLogger(__name__)` kullan, nereye yazılacağına programı kullanan karar
  versin.

## Özet

- Düzeyler `DEBUG < INFO < WARNING < ERROR < CRITICAL`; altındakiler yazılmaz.
- `basicConfig(level=..., format=...)` programın başında bir kez.
- Her modülde `log = logging.getLogger(__name__)`; adlar ağaç kurar, düzey
  ve kayıtlar yukarı akar.
- İşleyiciler: ekran (`StreamHandler`), dosya (`FileHandler`), her birinin
  düzeyi ve biçimi.
- `log.exception` hata iziyle; değerleri `"%s", x` ile ver, f-string ile değil.
