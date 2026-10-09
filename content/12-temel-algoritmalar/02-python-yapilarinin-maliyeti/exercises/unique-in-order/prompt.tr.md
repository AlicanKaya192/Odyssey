`unique_in_order(items)` fonksiyonunu yaz: listedeki tekrarları ayıklasın,
**her değerin ilk geçtiği sırayı** korusun.

- `[3, 1, 3, 2, 1]` → `[3, 1, 2]`
- `[]` → `[]`

**Hız şartı:** kod sonunda 100 000 elemanlı bir liste ayıklanıyor ve
alıştırmanın süresi 10 saniye. "Görüldü mü?" sorusunu **listeye** sorarsan
`O(n²)` olur ve süre yetmez; bir **küme** tut.

**Beklenen çıktı:**

```
[3, 1, 2]
50000
```
