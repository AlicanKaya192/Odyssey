Regex'in en sık kullanıldığı yerlerden biri **kayıt dosyası** (log)
ayrıştırmaktır: her satırı tarih, saat, düzey, bölüm ve mesaj diye
parçalara ayırıp saymak, süzmek. Uzun bir kalıbı okunur tutmanın yolu
**`re.VERBOSE`** bayrağı ve adlı gruplardır.

```python
import re

LOG = """2026-03-15 10:02:11 ERROR [db] connection lost
2026-03-15 10:02:15 INFO [web] request /home 200
2026-03-15 10:03:40 WARNING [db] slow query 2.4s
bad line without format
2026-03-15 10:05:02 ERROR [web] request /cart 500
2026-03-15 10:06:30 ERROR [db] connection lost"""

LINE = re.compile(r"""
    (?P<date>\d{4}-\d{2}-\d{2})\s
    (?P<time>\d{2}:\d{2}:\d{2})\s
    (?P<level>[A-Z]+)\s
    \[(?P<part>\w+)\]\s
    (?P<message>.+)
""", re.VERBOSE)

counts = {}
skipped = []
for line in LOG.splitlines():
    m = LINE.fullmatch(line)
    if m is None:
        skipped.append(line)
        continue
    key = (m["level"], m["part"])
    counts[key] = counts.get(key, 0) + 1
for key in sorted(counts):
    print(key, counts[key])
print("skipped:", skipped)
```

```text
('ERROR', 'db') 2
('ERROR', 'web') 1
('INFO', 'web') 1
('WARNING', 'db') 1
skipped: ['bad line without format']
```

## Neler oluyor?

- **`re.VERBOSE`**: kalıptaki boşluklar ve satır sonları yok sayılır (`#`
  ile yorum da yazılabilir). Her parçayı kendi satırına koyabildik. Bunun
  bedeli şu: gerçek bir boşluk aranacaksa **`\s`** (ya da `\ `) yazılır.
- **Adlı gruplar** kalıbı kendi kendini anlatır hâle getiriyor;
  `m["level"]` `m.group("level")`'ın kısa yazımı.
- `\[` ve `\]`: köşeli parantezin kendisi; ters bölü olmasa karakter sınıfı
  sanılırdı.
- **`fullmatch`**: satırın tamamı biçime uymalı. Uymayan satır sessizce
  atlanmadı, **`skipped`** listesine kondu. Gerçek kayıt dosyalarında biçim
  dışı satır hep çıkar; kaç tane olduğunu bilmek, kalıbın bir şeyi gözden
  kaçırıp kaçırmadığını gösterir.
- Sayaç olarak `(düzey, bölüm)` demeti anahtar: veritabanı bölümünde iki
  `ERROR` varmış.

Saymayı bir sonraki bölümdeki `collections.Counter` daha kısa yapıyor.
