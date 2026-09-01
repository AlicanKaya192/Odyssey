Elinde bir toplam ve bir sayı listesi var:

```python
total = 100
numbers = [10, 5, 0, 4]
```

Her sayı için `total / number` sonucunu yazdıracaksın. Ama listede bir `0`
duruyor ve sıfıra bölme hata veriyor:

```
ZeroDivisionError: division by zero
```

Program bu yüzden durmamalı. O sayıya gelince sonucu yazdıramıyorsan
`undefined` yazıp **listeye devam etmelisin**.

**Yapman gerekenler:**

1. Listeyi bir döngüyle gez.
2. Bölmeyi `try` bloğunun içine koy.
3. `ZeroDivisionError` çıkarsa sonuç yerine `undefined` yazdır.

**Beklenen çıktı:**

```
10.0
20.0
undefined
25.0
```

Sonuçlar ondalıklı çıkıyor çünkü `/` her zaman ondalıklı sayı veriyor.

> `if number != 0:` yazarak da bu çıktıyı elde edebilirsin ama bu alıştırma
> `try` / `except` üzerine; kontrol onu arıyor.
