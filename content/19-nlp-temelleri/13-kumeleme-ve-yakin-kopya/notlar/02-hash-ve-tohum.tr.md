Derste MinHash için Python'un hazır `hash()` fonksiyonu yerine
`zlib.crc32` kullandık. Sebebi: Python metinlerin özetini **her çalıştırmada
farklı** hesaplar. Aynı satırı iki ayrı Python sürecinde çalıştıralım:

```python
import os
import subprocess
import sys
import zlib

env = {k: v for k, v in os.environ.items() if k != "PYTHONHASHSEED"}
code = 'print(hash("strap"))'
runs = [subprocess.run([sys.executable, "-c", code], capture_output=True,
                       text=True, env=env).stdout.strip() for _ in range(2)]
print(runs[0] == runs[1])
print(zlib.crc32(b"strap"), zlib.crc32(b"strap"))
```

```text
False
3885747501 3885747501
```

- İki süreç "strap" için farklı sayı verdi. Python bunu bilerek yapıyor:
  özetler tahmin edilebilir olsaydı, kötü niyetli biri sözlüğe aynı kovaya
  düşen binlerce anahtar gönderip programı yavaşlatabilirdi. Rastgele bir
  tohum bunu önlüyor.
- Bir süreç içinde `hash()` tutarlı; sözlükler ve kümeler bu yüzden
  sorunsuz çalışır. Ama imzaları **kaydedip** başka bir gün, başka bir
  bilgisayarda karşılaştıracaksan sayıların her yerde aynı çıkması gerekir.
- `zlib.crc32` her makinede, her çalıştırmada aynı sayıyı verir. Gerçek
  sistemler MurmurHash ya da xxHash gibi daha hızlı ve dağılımı daha iyi
  özetler kullanır; fikir aynı.

`PYTHONHASHSEED` ortam değişkeniyle Python'un tohumunu sabitleyebilirsin,
ama bu sürecin bütün sözlüklerini etkiler ve unutulmaya çok açıktır.
Kalıcı bir sayı gerekiyorsa kararlı bir özet fonksiyonu kullan.
