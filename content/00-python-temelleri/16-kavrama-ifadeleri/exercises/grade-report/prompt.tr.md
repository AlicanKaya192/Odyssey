Bir sınıf raporu üreteceksin: kavrama ile hazırlayıp biçim belirteciyle
yazdıracaksın.

Elindeki veri:

```python
scores = {"ada": 90, "alan": 45, "grace": 72, "gauss": 38}
```

**Yapman gerekenler:**

1. `passed` — **50 ve üstü** alanların adları (liste, kavrama ile).
2. `average` — bütün notların ortalaması. `sum()` içine **üreteç ifadesi**
   yaz.
3. `lines` — her kişi için `"ada      90 ok"` biçiminde bir satır listesi:
   ad sola yaslı **8**, not sağa yaslı **3**, sonra bir boşluk ve
   `"ok"` / `"no"`.
4. Satırları döngüyle yazdır, sonra ortalamayı **bir ondalık basamakla**
   ve geçenleri yazdır.

**Beklenen çıktı:**

```
ada      90 ok
alan     45 no
grace    72 ok
gauss    38 no
Average: 61.2
Passed: ['ada', 'grace']
```

> Satır içinde hem koşullu değer hem biçim belirteci var:
> `f"{name:<8}{score:>3} " + ("ok" if score >= 50 else "no")` gibi
> yazabilirsin.
