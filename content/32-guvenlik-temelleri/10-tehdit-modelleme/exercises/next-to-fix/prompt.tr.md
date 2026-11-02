Her tehdit bir sözlük: `id`, `likelihood`, `impact`, `status`
(`"open"`, `"mitigated"` ya da `"accepted"`).

`next_to_fix(threats, n)` yalnızca **açık** (`"open"`) tehditlerden, puanı
(olasılık × etki) en yüksek `n` tanesinin kimliklerini döndürsün. Puanı
eşit olanlar kimliğe göre abece sırasında.

**Beklenen çıktı:**

```
['T1', 'T2']
['T1', 'T2', 'T4']
```
