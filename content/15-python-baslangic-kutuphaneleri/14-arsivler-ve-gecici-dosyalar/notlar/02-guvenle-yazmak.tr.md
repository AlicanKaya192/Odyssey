Bir ayar ya da kayıt dosyasının üstüne yazarken program yarıda kesilirse
(elektrik gider, program çöker) dosya **yarım** kalır: eski içerik gitmiş,
yenisi tamamlanmamış. Bunun yaygın çözümü **önce geçici dosyaya yazıp sonra
yer değiştirmektir**.

```python
import os
import tempfile
from pathlib import Path


def atomic_write(path, text, crash=False):
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        if crash:
            raise RuntimeError("power cut")
        os.replace(tmp, path)
    finally:
        Path(tmp).unlink(missing_ok=True)


settings = Path("settings.json")
settings.write_text('{"theme": "dark"}', encoding="utf-8")
with open(settings, "w", encoding="utf-8") as f:
    f.write('{"the')
print(settings.read_text(encoding="utf-8"))
settings.write_text('{"theme": "dark"}', encoding="utf-8")
try:
    atomic_write(settings, '{"theme": "light"}', crash=True)
except RuntimeError:
    print("crashed")
print(settings.read_text(encoding="utf-8"))
atomic_write(settings, '{"theme": "light"}')
print(settings.read_text(encoding="utf-8"))
print(sorted(p.name for p in Path(".").glob("*.tmp")))
```

```text
{"the
crashed
{"theme": "dark"}
{"theme": "light"}
[]
```

- İlk deneme doğrudan yazmanın sorununu gösteriyor: `open(..., "w")` dosyayı
  **açar açmaz boşaltır**; yazma yarıda kalınca elde `{"the` kaldı, geçerli
  bir JSON bile değil.
- **`atomic_write`** yeni içeriği aynı klasörde geçici bir dosyaya yazıyor
  (`mkstemp` benzersiz ad verir). Yazma bitmeden bir şey olursa (`crash=True`)
  asıl dosyaya **hiç dokunulmamış** oluyor: `{"theme": "dark"}` yerinde.
- Yazma bitince **`os.replace(geçici, asıl)`** geçici dosyayı asılın yerine
  koyar. Aynı diskte bu tek adımdır: dosyayı okuyan biri ya eskisini ya
  yenisini görür, yarımını hiç görmez.
- `finally` her durumda geçici dosyayı temizliyor; klasörde `.tmp` kalmadı.
- Geçici dosya **aynı klasörde** açılıyor: `os.replace` başka bir diske
  taşırken tek adım olamaz.

Bu desen ayar dosyalarında, önbelleklerde ve ilerleme kayıtlarında
kullanılır.
