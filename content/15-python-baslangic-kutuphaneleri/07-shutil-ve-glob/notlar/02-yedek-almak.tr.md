Bu bölümde öğrendiklerini birleştiren küçük bir araç: bir proje klasörünün
**tarihli yedeğini** alan ve yalnızca son birkaç yedeği tutan fonksiyon.

```python
import shutil
from datetime import datetime
from pathlib import Path

for name in ["project/main.py", "project/data/sales.csv", "project/debug.log"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")


def backup(source, root, now, keep=3):
    name = Path(source).name
    target = Path(root) / f"{name}-{now:%Y%m%d-%H%M}"
    shutil.copytree(source, target, ignore=shutil.ignore_patterns("*.log"))
    backups = sorted(Path(root).glob(f"{name}-*"))
    for old in backups[:-keep]:
        shutil.rmtree(old)
    return [b.name for b in sorted(Path(root).iterdir())]


for hour in [9, 12, 15, 18]:
    print(backup("project", "backups", datetime(2026, 3, 15, hour, 0)))
```

```text
['project-20260315-0900']
['project-20260315-0900', 'project-20260315-1200']
['project-20260315-0900', 'project-20260315-1200', 'project-20260315-1500']
['project-20260315-1200', 'project-20260315-1500', 'project-20260315-1800']
```

Neler oluyor:

- **Klasör adı tarihten:** `f"{now:%Y%m%d-%H%M}"` f-string'in içinde
  `strftime` biçimi kullanıyor. Yıl-ay-gün-saat sırası, adları **metin olarak
  sıralamayı tarih sırasıyla aynı** yapıyor; `sorted` en eskiyi başa koyuyor.
- **Kayıt dosyaları atlanıyor:** `ignore_patterns("*.log")`.
- **Son 3 yedek:** `backups[:-keep]` sondaki `keep` tane dışındakiler; onlar
  `rmtree` ile siliniyor. Dördüncü yedekte 09:00 yedeği gitti.
- **Saat parametre olarak geliyor:** fonksiyon `datetime.now()`'ı kendisi
  çağırmıyor. Böylece aynı girdiyle aynı sonucu veriyor ve sınanabiliyor;
  gerçek kullanımda `backup("project", "backups", datetime.now())` yazılır.

Gerçek bir yedek aracında bir adım daha olur: yedekler **başka bir diske**
(harici disk, ağ klasörü) alınır. Aynı diskteki yedek, disk bozulunca
projeyle birlikte gider.
