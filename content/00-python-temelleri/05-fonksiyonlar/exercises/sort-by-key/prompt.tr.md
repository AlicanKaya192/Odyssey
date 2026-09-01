`sorted` bir listeyi sıralıyor, ama elemanlar sözlük olduğunda "hangisi
büyük" sorusunu cevaplayamıyor. `key` tam bu soruyu cevaplıyor.

Elindeki veri:

```python
people = [
    {"name": "Grace", "grade": 75},
    {"name": "Ada", "grade": 90},
    {"name": "Brian", "grade": 40},
]
```

**Yapman gerekenler:**

1. `by_grade` adında bir fonksiyon yaz: bir sözlük alsın, `grade` değerini
   döndürsün.
2. `best_first` değişkeninde kişileri **nottan büyükten küçüğe** sıralı tut.
   `sorted` fonksiyonuna `key` ve `reverse` ver.
3. `names` değişkeninde bu sıradaki **adları** liste olarak tut.
4. `alphabetical` değişkeninde adları alfabetik sıralı liste olarak tut.
5. Önce `names`, sonra `alphabetical` yazdır.

**Beklenen çıktı:**

```
['Ada', 'Grace', 'Brian']
['Ada', 'Brian', 'Grace']
```

Dikkat: `key=by_grade` yazılıyor, `key=by_grade()` değil. Fonksiyonun
kendisini veriyorsun, sonucunu değil.

> Büyükten küçüğe sıralamak için `reverse=True` ekleniyor.
