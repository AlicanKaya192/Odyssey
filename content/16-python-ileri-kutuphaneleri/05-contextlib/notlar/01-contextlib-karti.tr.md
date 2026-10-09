## Sınıfla

```python
class Resource:
    def __enter__(self):
        # kur
        return self

    def __exit__(self, exc_type, exc, tb):
        # topla (hata olsa da olmasa da)
        return False   # True hatayı yutar
```

## Fonksiyonla

```python
from contextlib import contextmanager


@contextmanager
def resource():
    # kur
    try:
        yield "değer"
    finally:
        # topla
        ...
```

## contextlib

| Araç | Ne yapar |
|---|---|
| `@contextmanager` | üreteç fonksiyonunu bağlam yöneticisi yapar |
| `suppress(Hata)` | o hatayı yutar |
| `redirect_stdout(f)` / `redirect_stderr(f)` | çıktıyı başka yere yazar |
| `closing(nesne)` | sonda `nesne.close()` çağırır |
| `ExitStack()` | sayısı belli olmayan kaynakları toplar |
| `nullcontext(değer)` | hiçbir şey yapmayan yönetici |
| `chdir(klasör)` | çalışma klasörünü geçici değiştirir (3.11+) |

## Hazır bağlam yöneticileri

| Yazım | Toparladığı |
|---|---|
| `open(...)` | dosyayı kapatır |
| `with conn:` (sqlite3) | işlemi kaydeder ya da geri alır (kapatmaz!) |
| `tempfile.TemporaryDirectory()` | klasörü siler |
| `threading.Lock()` | kilidi bırakır |
| `decimal.localcontext()` | hassasiyet ayarını geri alır |

## Kural

Toparlama **`finally`** içinde; `yield` tek kez.
