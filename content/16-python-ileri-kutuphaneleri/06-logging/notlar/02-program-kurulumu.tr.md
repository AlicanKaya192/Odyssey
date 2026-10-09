Gerçek bir programda günlük kurulumu **tek bir fonksiyonda**, programın en
başında yapılır; modüller yalnızca `getLogger(__name__)` kullanır.

```python
import logging
import sys
from pathlib import Path


def setup_logging(log_file: str, verbose: bool = False) -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    file = logging.FileHandler(log_file, encoding="utf-8")
    file.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    root.handlers[:] = [console, file]


setup_logging("run.log")
log = logging.getLogger("report")
log.debug("rows loaded: %d", 120)
log.info("report ready")
for handler in logging.getLogger().handlers:
    handler.close()
print(Path("run.log").read_text(encoding="utf-8"))
```

```text
INFO: report ready
DEBUG report: rows loaded: 120
INFO report: report ready
```

- Kök kaydedici `DEBUG`'a açık; süzme işleyicilerde: ekran `INFO`'dan
  itibaren (ya da `verbose` ile her şey), dosya her şeyi alıyor. İlk satır
  ekranın, sonraki ikisi dosyanın.
- `root.handlers[:] = [...]` önceki işleyicileri değiştiriyor: fonksiyon iki
  kez çağrılsa da kayıtlar ikişer kez yazılmaz.
- `verbose` bir komut satırı seçeneğinden gelir (`--verbose`); bir sonraki
  bölümdeki `argparse` ile kurulur.

## Kontrol listesi

- Her modülde `log = logging.getLogger(__name__)`.
- Kurulum programın girişinde bir kez (`if __name__ == "__main__":`).
- Ekrana kısa, dosyaya ayrıntılı; dosyada zaman (`%(asctime)s`) olsun.
- Kullanıcının parolası, kişisel verisi, tam kredi kartı numarası gibi
  bilgiler günlüğe yazılmaz: günlük dosyaları paylaşılır ve saklanır.
- `print` yalnızca programın asıl çıktısı içindir; durum mesajları günlüğe.
