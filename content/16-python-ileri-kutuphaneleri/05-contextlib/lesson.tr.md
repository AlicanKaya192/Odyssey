# contextlib

`with open(...) as f:` yazdığında Python dosyayı blok bitince **ne olursa
olsun** kapatır: blok normal bitse de, içinde hata çıksa da. Bu söz veren
nesneye **bağlam yöneticisi** (context manager) denir. Dosya dışında da
"başla, iş bitince mutlaka toparla" gereken çok yer var: bir ayarı geçici
değiştirip eski hâline getirmek, süre ölçmek, kilit almak bırakmak, geçici
klasöre girip çıkmak. Bu bölümde kendi bağlam yöneticini yazmayı ve
**`contextlib`**'in hazır araçlarını görüyoruz.

## with nasıl çalışır?

```python
class Tracker:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"enter {self.name}")
        return self

    def __exit__(self, exc_type, exc, tb):
        print(f"exit {self.name}", exc_type.__name__ if exc_type else None)
        return False


with Tracker("a") as t:
    print("inside", t.name)
try:
    with Tracker("b"):
        raise ValueError("boom")
except ValueError as error:
    print("caught", error)
```

```text
enter a
inside a
exit a None
enter b
exit b ValueError
caught boom
```

- Bloğa girerken **`__enter__`** çağrılır; döndürdüğü değer `as`'tan sonraki
  ada bağlanır.
- Bloktan çıkarken **`__exit__`** her durumda çağrılır. Hata çıktıysa
  türünü, kendisini ve izini argüman olarak alır (`ValueError`); hata yoksa
  üçü de `None`.
- `__exit__` `False` döndürürse hata dışarı devam eder (yakalandı); `True`
  döndürürse hata yutulur. Yutmak nadiren doğrudur.

## @contextmanager: fonksiyonla bağlam yöneticisi

Sınıf yazmak uzun; çoğu zaman **`@contextmanager`** ile üreteç fonksiyonu
yeter:

```python
import time
from contextlib import contextmanager


@contextmanager
def timer(label, results):
    start = time.perf_counter()
    try:
        yield
    finally:
        results[label] = time.perf_counter() - start


@contextmanager
def temporary_setting(settings, key, value):
    old = settings[key]
    settings[key] = value
    try:
        yield settings
    finally:
        settings[key] = old


results = {}
with timer("sleep", results):
    time.sleep(0.05)
print(round(results["sleep"], 2))
settings = {"debug": False}
with temporary_setting(settings, "debug", True) as s:
    print(s)
print(settings)
try:
    with temporary_setting(settings, "debug", True):
        raise RuntimeError("fail")
except RuntimeError:
    print("after error", settings)
```

```text
0.05
{'debug': True}
{'debug': False}
after error {'debug': False}
```

- **`yield`**'den önceki kısım `__enter__`, sonraki kısım `__exit__` gibi
  çalışır; `yield`'in verdiği değer `as`'tan sonraki ada gider.
- Toparlama **`finally`** içinde: blokta hata çıksa da ayar eski hâline
  döndü (`after error` satırı). Bu, bölümün en önemli kuralı; sonunda
  unutulmuş hâlini görüyoruz.

## Hazır araçlar: suppress, redirect_stdout

```python
import io
from contextlib import redirect_stdout, suppress
from pathlib import Path

with suppress(FileNotFoundError):
    Path("missing.txt").unlink()
print("still running")
buffer = io.StringIO()
with redirect_stdout(buffer):
    print("captured line")
print(repr(buffer.getvalue()))
```

```text
still running
'captured line\n'
```

- **`suppress(HataTürü)`** o hatayı sessizce yutar: "dosya varsa sil, yoksa
  önemli değil". `try/except: pass` yazmanın kısa ve niyeti açık yolu.
  Yalnızca beklediğin hata türünü ver.
- **`redirect_stdout(hedef)`** blok boyunca `print`'leri ekran yerine başka
  bir yere yazar; çıktısını yakalamak istediğin bir fonksiyonu sınarken işe
  yarar. `io.StringIO` bellekte bir metin dosyası gibi davranır.

## ExitStack: sayısı belli olmayan kaynaklar

```python
from contextlib import ExitStack
from pathlib import Path

for i in range(3):
    Path(f"part{i}.txt").write_text(f"line {i}\n", encoding="utf-8")
with ExitStack() as stack:
    paths = [f"part{i}.txt" for i in range(3)]
    files = [stack.enter_context(open(p, encoding="utf-8")) for p in paths]
    merged = [f.readline().strip() for f in files]
print(merged, all(f.closed for f in files))
```

```text
['line 0', 'line 1', 'line 2'] True
```

Kaç dosya açılacağı önceden belli değilse iç içe `with` yazılamaz.
**`ExitStack`** her `enter_context` ile açılanı hatırlar ve blok bitince
hepsini (ters sırayla) kapatır; aradaki birinin açılması hata verse bile
öncekiler kapanır.

## chdir ve nullcontext

```python
from contextlib import chdir, nullcontext
from pathlib import Path

Path("sub").mkdir()
before = Path.cwd().name
with chdir("sub"):
    print(Path.cwd().name)
print(Path.cwd().name == before)


def maybe(manager=None):
    return manager if manager is not None else nullcontext()


with maybe() as value:
    print("no manager needed", value)
```

```text
sub
True
no manager needed None
```

- **`chdir(klasör)`** (Python 3.11+) blok boyunca çalışma klasörünü
  değiştirir, sonra eskisine döner.
- **`nullcontext()`** hiçbir şey yapmayan bağlam yöneticisidir: kod `with`
  bekliyorsa ama bazen gerçek bir kaynak yoksa, `if` ile iki ayrı kod yazmak
  yerine kullanılır.

## Sık hata: finally'siz toparlama

```python
from contextlib import contextmanager


@contextmanager
def careless(log):
    log.append("open")
    yield
    log.append("close")


log = []
try:
    with careless(log):
        raise KeyError("x")
except KeyError:
    pass
print(log)
```

```text
['open']
```

Blokta hata çıkınca hata `yield` satırında yeniden fırlatılır ve sonraki
satırlar **çalışmaz**: `close` hiç yazılmadı. Gerçek bir programda bu,
kapatılmayan bir dosya, bırakılmayan bir kilit ya da eski hâline dönmeyen
bir ayar demek. `yield`'i her zaman `try/finally` içine al.

## Özet

- `with` = `__enter__` (başta) + `__exit__` (sonda, her durumda).
- `@contextmanager`: `yield`'den önce kurulum, `finally`'de toparlama.
- `suppress(Hata)`: beklenen hatayı yut; `redirect_stdout`: çıktıyı yakala.
- `ExitStack`: sayısı belli olmayan kaynaklar; `chdir`, `nullcontext`.
- Toparlamayı `finally`'ye yaz; yoksa hata çıkınca çalışmaz.
