Dil modeli yalnızca metin üretmek için değil, metni **yargılamak** için de
kullanılır: hangi cümle daha doğal? Dersteki bigram modeli (`logprob`) ile
500 test talebini kelimeleri karıştırılmış hâlleriyle karşılaştıralım:

```python
import random

rng = random.Random(1)
wins = total = 0
for s in test[:500]:
    words = s[1:-1]
    shuffled = rng.sample(words, len(words))
    if shuffled != words:
        total += 1
        wins += logprob(words) > logprob(shuffled)
print(wins, total)
```

```text
500 500
```

- 500 talebin 500'ünde model gerçek sırayı karışık sıradan daha olası
  buldu. Yalnızca bir önceki kelimeye bakan bir model bile kelime sırası
  hakkında çok şey biliyor.
- Aynı fikir yazım düzeltmede kullanılır: "there is my order" ile "where is
  my order" arasında dil modeli hangisinin daha olası olduğunu söyler.
  Konuşma tanıma da, akustik olarak benzer adaylar arasında dil modelinin
  daha olası bulduğunu seçer.
- Dikkat: olasılık cümle uzadıkça küçülür. Farklı uzunluktaki cümleleri
  karşılaştırırken toplam log olasılığı değil, kelime başına ortalamayı
  (ya da şaşkınlığı) kullan.
