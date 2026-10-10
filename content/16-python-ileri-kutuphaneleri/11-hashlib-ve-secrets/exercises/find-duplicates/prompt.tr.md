`duplicates(paths)` içeriği **aynı** olan dosyaları bulsun: her dosyanın
SHA-256 özetini al, aynı özete sahip yolları grupla. Yalnızca **birden çok**
dosyası olan grupları döndür; her grup sıralı bir liste, gruplar da ilk
elemanlarına göre sıralı olsun.

**Beklenen çıktı:**

```
['files/a.txt', 'files/c.txt']
['files/b.txt', 'files/d.txt']
```
