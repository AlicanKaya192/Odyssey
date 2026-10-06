**Asal sayı**, 1'den büyük olup yalnızca 1'e ve kendisine tam bölünen
sayıdır: 2, 3, 5, 7, 11… Aralarındaki fark 2 olan iki asala **ikiz asal**
denir: (3, 5), (5, 7), (11, 13)…

`2`'den `100`'e kadar (100 dahil):

1. Kaç asal sayı olduğunu `prime_count` değişkeninde say.
2. Bu aralıktaki **en büyük** ikiz asal çiftini `twin_a` ve `twin_b`
   değişkenlerinde bul.

```
Primes up to 100 : 25
Largest twin pair: 71 73
```

Bu alıştırmada iki döngü iç içe çalışıyor:

- **Dıştaki döngü** 2'den 100'e kadar her sayıyı tek tek ele alıyor.
- **İçteki döngü** o sayının asal olup olmadığına bakıyor: 2'den başlayıp
  kendisinden küçük sayılara bölmeyi deniyor. Biri tam bölerse sayı asal
  değil; `break` ile aramayı bırakabilirsin.

İkiz çiftleri için bir değişkende **bir önceki asalı** tut. Yeni bir asal
bulduğunda farkları 2 ise bir ikiz çifti buldun demektir. Sayılar küçükten
büyüğe gittiği için son bulduğun çift en büyüğü olacak.

> Dikkat: Asal olup olmadığını anlamak için önce "asal" diye başlayan bir
> işaret değişkeni (`is_prime = True`) kur, bölen bulursan `False` yap.
> Bu işareti her yeni sayıda **yeniden** `True` yapmayı unutma.
