`fit_middle(text, max_words)` metin `max_words` kelimeyi geçmiyorsa onu
olduğu gibi döndürsün. Geçiyorsa ilk `max_words // 2` kelimeyi ve son
`max_words - max_words // 2` kelimeyi tutsun, aralarına `" ... "` koysun.
Kelimeler `text.split()` ile bölünür, tek boşlukla birleştirilir.

**Beklenen çıktı:**

```
one two ... six seven
short text
```
