`common_elements(a, b)` fonksiyonunu yaz: iki listede de geçen değerleri
**küçükten büyüğe sıralı ve tekrarsız** bir liste olarak döndürsün.

- `[1, 2, 2, 3]` ve `[2, 3, 4]` → `[2, 3]`

**Hız şartı:** kodun sonunda 100 000 ve 66 667 elemanlı iki liste
karşılaştırılıyor ve süre 10 saniye. İç içe döngü `O(n × m)` olur;
listelerden birini **kümeye** çevir, öbürünün elemanlarına orada bak.
Sonucu sıralamak için `sorted` kullanabilirsin.

**Beklenen çıktı:**

```
[2, 3]
33334
```
