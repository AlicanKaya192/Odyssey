Beş öğrencinin üç sınav notu bir matriste: satır öğrenci, sütun sınav. Bu
bölümün araçlarıyla tek satırlık cevaplar:

```python
import numpy as np

names = np.array(["ada", "alan", "grace", "linus", "guido"])
scores = np.array([[72, 88, 95], [55, 61, 70], [90, 94, 85],
                   [40, 75, 62], [83, 79, 91]])
passed_all = (scores >= 60).all(axis=1)
print(names[passed_all].tolist())
print(names[scores.argmax(axis=0)].tolist())
mean = scores.mean(axis=1)
print(names[np.argsort(mean)[::-1]][:3].tolist())
curved = np.where(scores < 60, 60, scores)
print(int(curved.sum() - scores.sum()))
ranks = np.argsort(np.argsort(-mean)) + 1
print(dict(zip(names.tolist(), ranks.tolist())))
```

```text
['ada', 'grace', 'guido']
['grace', 'grace', 'ada']
['grace', 'ada', 'guido']
25
{'ada': 2, 'alan': 4, 'grace': 1, 'linus': 5, 'guido': 3}
```

## Satır satır

| Soru | Yazım |
|---|---|
| Bütün sınavlardan geçenler | `(scores >= 60).all(axis=1)` maskesiyle `names[...]` |
| Her sınavın birincisi | `scores.argmax(axis=0)` → her sütunda en büyüğün satırı |
| Ortalamaya göre ilk üç | `np.argsort(mean)[::-1][:3]` |
| 60'ın altını 60'a çekmek | `np.where(scores < 60, 60, scores)`; eklenen puan 25 |
| Sıra numarası (1 = en iyi) | `np.argsort(np.argsort(-mean)) + 1` |

## İki kez argsort

`argsort` bir kez "sıralı dizide hangi eleman nerede" sorusuna cevap verir
(`[2, 0, 4, 1, 3]`: önce grace, sonra ada...). İkinci kez `argsort` bunu tersine
çevirir: "her eleman sıralı dizide kaçıncı" (`ada` 1. konumda, yani 2.). Eksi
işareti büyükten küçüğe sıralamak içindir.

## Neden döngü yok?

Aynı soruları `for` döngüleriyle de yazabilirdin; NumPy'de her biri tek
ifade ve C hızında. Veri büyüdükçe fark büyür: binlerce öğrenci ve yüzlerce
sınavda döngü saniyeler, dizi işlemi milisaniyeler sürer.
