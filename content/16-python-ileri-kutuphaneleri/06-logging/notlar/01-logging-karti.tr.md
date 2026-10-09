## Düzeyler

| Düzey | Sayı | Ne için |
|---|---|---|
| `DEBUG` | 10 | geliştiricinin ayrıntısı |
| `INFO` | 20 | olağan olaylar (başladı, bitti) |
| `WARNING` | 30 | beklenmedik ama sürüyor (varsayılan eşik) |
| `ERROR` | 40 | bir iş yapılamadı |
| `CRITICAL` | 50 | program sürdürülemiyor |

## Kurulum

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)
```

## Kaydetmek

| Yazım | Ne yapar |
|---|---|
| `log.info("x=%s", x)` | değer ayrı argüman |
| `log.exception("...")` | `except` içinde, hata iziyle |
| `log.setLevel(logging.DEBUG)` | bu kaydedicinin eşiği |
| `log.getEffectiveLevel()` | ağaçtan gelen geçerli düzey |

## İşleyiciler

| Sınıf | Nereye |
|---|---|
| `StreamHandler(sys.stdout)` | ekran |
| `FileHandler("a.log", encoding="utf-8")` | dosya |
| `handlers.RotatingFileHandler(..., maxBytes=, backupCount=)` | büyüyünce yeni dosya |
| `handlers.TimedRotatingFileHandler(..., when="midnight")` | her gün yeni dosya |

Her işleyiciye `setLevel` ve `setFormatter(logging.Formatter(...))`.

## Biçim alanları

`%(asctime)s` zaman, `%(levelname)s` düzey, `%(name)s` kaydedici,
`%(message)s` mesaj, `%(funcName)s` fonksiyon, `%(lineno)d` satır,
`%(module)s` modül.
