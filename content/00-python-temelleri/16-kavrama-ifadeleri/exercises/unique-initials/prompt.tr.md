Tekrarsız bir küme üreteceksin.

Elindeki veri:

```python
words = ["Ada", "alan", "Grace", "ada", "Gauss"]
```

**Yapman gerekenler:**

1. `initials` — kelimelerin **küçük harfe çevrilmiş** ilk harfleri, küme
   olarak (tekrarsız).
2. `unique` — kelimelerin küçük harfli hâlleri, küme olarak.
3. İkisini de `sorted()` ile sıralayıp yazdır — kümenin sırası garanti
   olmadığı için.

**Beklenen çıktı:**

```
['a', 'g']
['ada', 'alan', 'gauss', 'grace']
```

> `sorted(initials)` kümeyi sıralı bir listeye çeviriyor; küme kavramasını
> yine de kendin yazacaksın.
