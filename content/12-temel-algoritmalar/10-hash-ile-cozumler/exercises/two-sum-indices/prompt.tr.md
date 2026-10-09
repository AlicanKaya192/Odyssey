`two_sum(numbers, target)` fonksiyonunu yaz: **sırasız** listede toplamı
`target` olan iki elemanın **indekslerini** `(i, j)` demeti olarak döndürsün
(`i < j`); yoksa `None`.

Her `x` için tümleyeni `target - x` daha önce görüldü mü diye bir sözlüğe
(değer → indeks) sor.

**Hız şartı:** kodun sonunda 200 000 sayılık listede olmayan bir toplam
aranıyor; iç içe döngü süreye yetişmez.

**Beklenen çıktı:**

```
(3, 4)
(0, 1)
None
```
