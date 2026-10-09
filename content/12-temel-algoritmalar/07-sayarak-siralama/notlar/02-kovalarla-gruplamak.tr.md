Sayarak sıralamanın fikri (değeri doğrudan adres yapmak) veri işinde her
gün kullanılır. Python'da bunun hazır araçları var.

## Histogram: `collections.Counter`

```python
from collections import Counter

grades = ["B", "A", "C", "B", "B", "A"]
counts = Counter(grades)
print(counts["B"])               # 3
print(counts.most_common(2))     # [('B', 3), ('A', 2)]
```

`Counter` bir sözlük; aralık sınırlı olmak zorunda değil, değerler metin de
olabilir. Kurmak `O(n)`.

## Gruplamak: `defaultdict(list)`

```python
from collections import defaultdict

students = [("Ada", "A"), ("Bora", "B"), ("Cem", "A"), ("Deniz", "C")]
by_grade = defaultdict(list)
for name, grade in students:
    by_grade[grade].append(name)
print(dict(by_grade))   # {'A': ['Ada', 'Cem'], 'B': ['Bora'], 'C': ['Deniz']}
```

Her grup girdideki sırayı korur. Kovalar sözlükte olduğu için anahtarların
sayı ve küçük aralıkta olması gerekmez.

## Dikkat: `itertools.groupby` sıralı veri ister

`groupby` yalnızca **yan yana** duran eşit anahtarları bir araya toplar.
Veri sıralı değilse aynı anahtar birden çok grupta çıkar:

```python
from itertools import groupby

letters = ["a", "b", "a"]
print([key for key, _ in groupby(letters)])            # ['a', 'b', 'a']
print([key for key, _ in groupby(sorted(letters))])    # ['a', 'b']
```

Sıralı olmayan veride gruplamak için `defaultdict` daha güvenli ve `O(n)`.

## pandas karşılığı

Veri Bilimi patikasındaki `value_counts()` histogramın, `groupby()` ise
kovalarla gruplamanın tablo hâlidir; içlerinde aynı hash ve kova fikri
çalışır.
