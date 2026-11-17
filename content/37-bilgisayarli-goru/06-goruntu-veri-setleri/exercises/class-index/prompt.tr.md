`class_index(names)` geçici bir klasörde her ad için bir alt klasör açıp içine
boş (4 × 4, siyah) bir PNG koysun, sonra `datasets.ImageFolder` ile okuyup
`class_to_idx` sözlüğünü döndürsün. Sayı adlarında sıranın nasıl
değiştiğine bak.

**Beklenen çıktı:**

```
{'bird': 0, 'cat': 1, 'dog': 2}
{'12': 0, '3': 1, '7': 2}
```
