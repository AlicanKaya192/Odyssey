`letter_grades(scores)` fonksiyonunu yaz: her puanı harf notuna çevirsin:
60'ın altı `F`, 60–69 `D`, 70–79 `C`, 80–89 `B`, 90 ve üstü `A`. Sınırlar
`[60, 70, 80, 90]` listesinde, harfler `"FDCBA"` metninde;
`bisect.bisect(sınırlar, puan)` harfin indeksini verir.

**Beklenen çıktı:**

```
['F', 'A', 'C', 'C', 'B', 'D', 'F']
```
