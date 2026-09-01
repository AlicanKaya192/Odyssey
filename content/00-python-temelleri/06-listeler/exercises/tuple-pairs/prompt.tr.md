Demet, değiştirilemeyen bir liste. Birbirine ait sabit sayıda değeri
tutmak için kullanılıyor — bir nokta, bir isim-not çifti gibi.

**Yapman gerekenler:**

1. `point` adında bir **demet** tanımla: `(3, 7)`
2. `x` ve `y` değişkenlerine demeti tek satırda aç.
3. `pairs` adında bir liste tanımla; her elemanı bir isim-not **demeti**
   olsun:

```python
[("Ada", 90), ("Brian", 40), ("Grace", 75)]
```

4. `names` değişkeninde yalnızca adları liste olarak tut.
5. `best` değişkeninde en yüksek notu alan kişinin **demetini** tut.
6. Sırayla `point`, `x`, `y`, `names` ve `best` yazdır.

**Beklenen çıktı:**

```
(3, 7)
3
7
['Ada', 'Brian', 'Grace']
('Ada', 90)
```

Dikkat: `best` bir demet, adın kendisi değil — çıktıda parantezle
görünüyor.

> Demeti açmak: `x, y = point`. En yükseği bulmak için demetlerde
> dolaşıp not değerini karşılaştırabilirsin; demetin ikinci elemanı
> `pair[1]`.
