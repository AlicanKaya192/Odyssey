Kaç alıştırmanın çözüldüğünü yüzdesiyle birlikte yazdıracaksın.

Elindeki veri:

```python
solved = 24
total = 257
```

**Yapman gerekenler:**

1. `remaining` — kalan alıştırma sayısı.
2. `rate` — çözülenlerin oranı (`solved / total`). **Yüzle çarpma**,
   belirteç bunu kendisi yapıyor.
3. Aşağıdaki üç satırı yazdır; yüzdeler **bir ondalık basamaklı**.

**Beklenen çıktı:**

```
Solved: 24 / 257
Rate: 9.3%
Remaining: 233 (90.7%)
```

> `f"{rate:.1%}"` hem yüzle çarpar hem `%` işaretini koyar. `rate * 100`
> yazarsan sonuç yüz kat büyük çıkar.
