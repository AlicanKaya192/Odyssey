`tfidf_vectors(docs)` dersteki hesabı yapsın: dağarcık alfabetik sıralı;
her kelimenin IDF'i `ln((1 + n) / (1 + df)) + 1`; her belgede sayı × IDF;
sonra satırı L2 ile birim uzunluğa getir ve 3 basamağa yuvarla. Başlangıç
kodu yalnızca sayıları döndürüyor.

**Beklenen çıktı:**

```
[0.577, 0.577, 0.577, 0.0]
[0.707, 0.707, 0.0, 0.0]
[0.0, 0.0, 0.836, 0.549]
```
