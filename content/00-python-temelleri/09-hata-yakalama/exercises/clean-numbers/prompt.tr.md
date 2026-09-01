Bir yerden gelen veri hep temiz olmuyor. Elindeki listede sayıya
çevrilebilenler de var, çevrilemeyenler de:

```python
values = ["12", "7", "abc", "30", "5x"]
```

`int("abc")` çağrısı `ValueError` veriyor. Program bunun yüzünden durmamalı;
çevrilebilenleri toplayıp çevrilemeyenleri saymalı.

**Yapman gerekenler:**

1. İki değişken oluştur:

| Değişken | İçinde ne olacak |
|---|---|
| `total` | Sayıya çevrilebilenlerin toplamı |
| `skipped` | Çevrilemeyenlerin sayısı |

2. Listeyi gez. Her değeri sayıya çevirmeyi **dene**; olmuyorsa say ve devam et.
3. Önce `total`, sonra `skipped` yazdır.

**Beklenen çıktı:**

```
49
2
```

`12 + 7 + 30 = 49`; `"abc"` ve `"5x"` çevrilemiyor.

> `"5x"` ilk bakışta çevrilebilir görünüyor ama `int()` metnin **tamamının**
> sayı olmasını istiyor. Sondaki harf yüzünden o da `ValueError` veriyor.
