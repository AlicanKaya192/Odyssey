Sözlükleri kavramayla kuracaksın.

Elindeki veri:

```python
words = ["ada", "alan", "grace"]
scores = {"ada": 90, "alan": 45, "grace": 72}
```

**Yapman gerekenler — üçünü de kavrama ile yaz:**

1. `lengths` — her kelimenin uzunluğu (`{kelime: uzunluk}`).
2. `passed` — `scores` içinden **50 ve üstü** olanlar.
3. `flipped` — `scores`'un anahtarıyla değeri yer değişmiş hâli.

Sonra üçünü sırayla yazdır.

**Beklenen çıktı:**

```
{'ada': 3, 'alan': 4, 'grace': 5}
{'ada': 90, 'grace': 72}
{90: 'ada', 45: 'alan', 72: 'grace'}
```

> Sözlükte dönmek için `scores.items()` kullanılıyor; bu sana her turda
> iki değer veriyor.
