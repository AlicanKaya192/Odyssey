`max_window_sum(values, k)` fonksiyonunu **kayan pencereyle** yaz: **art
arda** `k` elemanın toplamlarının en büyüğünü döndürsün. `k <= 0` ya da `k`
liste boyundan büyükse `None`.

- `[2, -1, 3, 5, -2, 4]`, `k = 3`: pencereler `4`, `7`, `6`, `7` → `7`

Son satırdaki büyük girdi `O(n²)` bir çözümü süre sınırına takar; `O(n)` gerekir. Her pencereyi `sum` ile baştan toplamak `O(n × k)`.

**Beklenen çıktı:**

```
7
None
1659
```
