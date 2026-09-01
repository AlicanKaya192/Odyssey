Bir listeden başka bir liste üretmenin tek satırlık yazımını
kullanacaksın. Gerçek kodda çok yaygın; okuyabilmen gerekiyor.

Elindeki veri:

```python
scores = [90, 40, 75, 30, 65]
names = ["ada", "alan", "grace"]
```

**Yapman gerekenler — hepsini liste üreteci ile yaz, döngü kurma:**

1. `doubled` — her notun iki katı.
2. `passed` — yalnızca **50 ve üstü** notlar.
3. `upper_names` — bütün adlar büyük harfle.
4. `short_names` — yalnızca **beş harften kısa** adlar, büyük harfle.

Sonra dördünü sırayla yazdır.

**Beklenen çıktı:**

```
[180, 80, 150, 60, 130]
[90, 75, 65]
['ADA', 'ALAN', 'GRACE']
['ADA', 'ALAN']
```

> Yazım şöyle: `[ifade for eleman in liste]`. Süzmek için sonuna
> `if kosul` ekleniyor. Büyük harf için `name.upper()`.
