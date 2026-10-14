`context_share(doc_id, doc_ids)` salt okunur `doc_data.py`'deki
makalelerle çalışsın: `doc_id` makalesinin metninin token sayısını ve
`doc_ids`'teki bütün makalelerin metinlerinin toplam token'ını
`count_tokens` ile bulsun. Döndür: `[tek, hepsi, tek / hepsi]`; oran 2
basamağa yuvarlanmış.

**Beklenen çıktı:**

```
[94, 361, 0.26]
[50, 361, 0.14]
```
