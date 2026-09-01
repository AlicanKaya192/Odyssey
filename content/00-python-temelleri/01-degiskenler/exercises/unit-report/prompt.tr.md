Değişkenler, tip dönüşümü ve f-string'i bir arada kullanacaksın.

Elinde ölçüler **metin** olarak duruyor — gerçek hayatta veri böyle geliyor:

```python
raw_height = "180"
raw_weight = "75.5"
name = "Ada"
```

**Yapman gerekenler:**

1. `height` değişkeninde boyu **tam sayı** olarak tut.
2. `weight` değişkeninde kiloyu **ondalıklı sayı** olarak tut.
3. `meters` değişkeninde boyu metre cinsinden tut (santimetreyi 100'e böl).
4. `bmi` değişkeninde vücut kütle indeksini tut: kilo bölü metre karesi,
   **iki basamağa yuvarlanmış**.
5. Tek satırda, **f-string kullanarak** şunu yazdır:

```
Ada is 1.8 m and 75.5 kg, bmi 23.3
```

**Beklenen çıktı:**

```
Ada is 1.8 m and 75.5 kg, bmi 23.3
```

Dikkat: hiçbir sayıyı elle yazma, hepsi hesaplanacak.

> `int("180")` metni tam sayıya, `float("75.5")` ondalıklıya çeviriyor.
> `round(deger, 2)` iki basamağa yuvarlıyor. f-string içinde değişken
> süslü parantezle yazılıyor: `f"{name} is ..."`
