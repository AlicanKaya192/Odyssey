İki dersin öğrenci listeleri **küme** olarak verilmiş:

```python
class_a = {"Ada", "Alan", "Grace", "Linus", "Guido"}
class_b = {"Grace", "Guido", "Margaret", "Linus", "Dennis", "Ken"}
```

Şunları bul:

- `both`: iki derse de giden öğrenciler
- `only_a`: yalnızca A dersine gidenler
- `only_b`: yalnızca B dersine gidenler
- `total`: en az bir derse giden **farklı** öğrenci sayısı

```
Both: ['Grace', 'Guido', 'Linus']
Only A: ['Ada', 'Alan']
Only B: ['Dennis', 'Ken', 'Margaret']
Total: 8
```

Kümelerin işlemleri bunu tek satırlara indiriyor: kesişim `&`, fark `-`,
birleşim `|`. Önce her birinin ne verdiğini kâğıtta düşün: `class_a -
class_b` ile `class_b - class_a` aynı şey mi?

> Dikkat: Kümenin elemanları her çalıştırmada aynı sırada yazdırılmayabilir.
> Bu yüzden yazdırırken `sorted()` ile sıralı bir listeye çevir. `total`
> için iki kümenin uzunluklarını toplarsan iki derse birden gidenleri iki
> kez saymış olursun.
