`max_subarray(values)` fonksiyonunu **Kadane** ile, tek geçişte yaz: en büyük
toplamlı alt dizinin (art arda, en az bir eleman) toplamını döndürsün.

`current` burada biten en iyi toplam: `current = max(x, current + x)`;
`best` şimdiye kadarkilerin en büyüğü.

Son satır bir milyon elemanlı; her başlangıç–bitiş çiftini deneyen `O(n²)`
çözüm süre sınırına takılır.

**Beklenen çıktı:**

```
7
-1
591
```
