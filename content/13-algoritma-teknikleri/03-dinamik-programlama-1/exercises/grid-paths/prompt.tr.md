`grid_paths(grid)` fonksiyonunu yaz: `grid` metinlerden oluşan bir liste,
`.` boş hücre, `#` engel. Sol üstten sağ alta yalnızca **sağa ve aşağı**
giderek kaç yol olduğunu döndürsün. Başlangıç ya da bitiş engelliyse `0`.

`paths[r][c] = üst + sol`, engelli hücre `0`.

Son ızgara 18 × 18; bütün yolları tek tek gezmek milyarlarca yol demek,
tablo gerekir.

**Beklenen çıktı:**

```
6
2
0
2333606220
```
