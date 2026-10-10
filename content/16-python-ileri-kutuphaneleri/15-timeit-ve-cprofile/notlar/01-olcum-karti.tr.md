## timeit

| Yazım | Ne yapar |
|---|---|
| `timeit.timeit("kod", setup="...", number=1000)` | toplam süre (sn) |
| `timeit.timeit(fonksiyon, number=10)` | fonksiyonu ölç |
| `min(timeit.repeat(..., number=n, repeat=5))` | en güvenilir tek değer |
| `python -m timeit -s "kurulum" "kod"` | komut satırı |

## cProfile ve pstats

| Yazım | Ne yapar |
|---|---|
| `p = cProfile.Profile(); p.enable() ... p.disable()` | bir bölümü profille |
| `p.runcall(f, x)` | tek çağrıyı profille |
| `pstats.Stats(p).sort_stats("cumulative").print_stats(10)` | ilk 10 satırı yazdır |
| `sort_stats("tottime")` | kendi süresine göre |
| `python -m cProfile -s cumtime app.py` | bütün program |
| `-o profile.out` | sonucu dosyaya yaz |

## Sütunlar

| Sütun | Anlamı |
|---|---|
| `ncalls` | kaç kez çağrıldı |
| `tottime` | fonksiyonun kendi içinde geçen süre |
| `cumtime` | çağırdıkları dahil toplam süre |
| `percall` | süre / çağrı |

## Sıra

1. Sonucu doğrulayan bir test ya da karşılaştırma hazırla.
2. Profille, en büyük `cumtime` / `tottime` kalemini bul.
3. Yalnızca onu düzelt.
4. Sonuç aynı mı? Yeniden ölç.
