`count_prefix(words, prefixes)` fonksiyonunu **trie** ile yaz: her önek için
o önekle başlayan kelime sayısını, öneklerle aynı sırada bir liste olarak
döndürsün. Boş önek bütün kelimeleri sayar.

Her düğümde `"#"` anahtarına o düğümden geçen kelime sayısını yaz; sorguda
önekin düğümüne in ve sayıyı oku. `startswith` yok.

**Beklenen çıktı:**

```
[4, 5, 3, 0, 8]
```
