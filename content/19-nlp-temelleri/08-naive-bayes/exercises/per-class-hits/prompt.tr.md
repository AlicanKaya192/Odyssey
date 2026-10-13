`per_class_hits(ngrams)` verilen `ngram_range` ile bir `CountVectorizer` ve
`MultinomialNB` kursun ve test verisinde **her sınıfın** örneklerinin ne
kadarının doğru bulunduğunu (3 basamak) sınıf adından oranına bir sözlükte,
sınıflar alfabetik sırayla döndürsün. `ngrams` liste olarak da
gelebilir; `tuple(ngrams)` ile ver. Hangi sınıf en zor, kelime çiftleri
hangisine yardım ediyor?

**Beklenen çıktı:**

```
(1, 1)
   account 0.942
   billing 0.924
   refund 0.87
   shipping 0.932
   technical 0.935
(1, 2)
   account 0.951
   billing 0.962
   refund 0.87
   shipping 0.939
   technical 0.952
```
