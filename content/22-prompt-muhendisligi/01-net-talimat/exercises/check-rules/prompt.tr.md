`check(text, rules)` cevabın kaldığı kuralların adlarını bu sırayla bir
liste olarak döndürsün: `max_words`, `max_sentences`, `must_include`,
`must_not_include`. Sözlükte olmayan kural denetlenmez. Cümleler
`re.split(r"[.!?]+", text)` ile bölünür, boş parçalar sayılmaz;
`must_include` büyük/küçük harfe duyarsız, `must_not_include` duyarlı.

**Beklenen çıktı:**

```
ok
['max_sentences', 'must_not_include']
['must_include']
```
