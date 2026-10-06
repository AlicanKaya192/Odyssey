İki değişkenin değerleri yanlış yerde:

```python
left = "pear"
right = "apple"
```

Değerleri yer değiştir: sonunda `left` içinde `"apple"`, `right` içinde
`"pear"` olsun. Sonra ikisini yazdır:

```
apple pear
```

Kural: `"apple"` ve `"pear"` metinlerini **yeniden yazma**. Değerleri
değişkenler arasında taşı.

> Dikkat: En sık yapılan hata `left = right` yazıp ardından
> `right = left` yazmak. Bunu yaparsan ikisi de aynı değeri taşır, çünkü
> ilk satır `left`'in eski değerini sildi. Eski değeri bir yerde saklaman
> gerekiyor.
