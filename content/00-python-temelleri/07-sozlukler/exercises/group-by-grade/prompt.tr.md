Öğrencilerin notları bir sözlükte:

```python
grades = {"Ada": "A", "Alan": "B", "Grace": "A", "Linus": "C", "Guido": "B", "Ken": "A"}
```

Bu sözlüğü **ters çevir**: anahtarı not, değeri o notu alan öğrencilerin
listesi olan `by_grade` sözlüğünü kur:

```python
{"A": ["Ada", "Grace", "Ken"], "B": ["Alan", "Guido"], "C": ["Linus"]}
```

Sonra her notu öğrencileriyle birlikte, notlar alfabetik sırada olacak
şekilde yazdır:

```
A: ['Ada', 'Grace', 'Ken']
B: ['Alan', 'Guido']
C: ['Linus']
```

Düz bir ters çevirme (`by_grade[grade] = name`) işe yaramaz: aynı notu alan
ikinci öğrenci birincinin üzerine yazar. Her not için bir **liste** tutup
öğrencileri ona eklemen gerekiyor; o notun listesi henüz yoksa önce boş bir
liste açmalısın.

> Dikkat: Öğrencilerin listedeki sırası `grades` sözlüğündeki sıralarıyla
> aynı kalmalı (`Ada`, `Grace`, `Ken`).
