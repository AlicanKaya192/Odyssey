`greedy(sentences, max_len)` bigram sayımlarıyla `<s>`'den başlayıp her adımda
**en sık** sonraki kelimeyi seçsin (eşitlikte abece sırası). `</s>` gelince
ya da `max_len` kelimeye ulaşınca dursun; üretilen kelimeleri (`<s>` ve
`</s>` hariç) döndürsün.

**Beklenen çıktı:**

```
['my', 'order', 'is', 'late']
['my', 'order']
```
