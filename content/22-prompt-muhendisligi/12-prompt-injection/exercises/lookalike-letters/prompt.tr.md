`detect_normalized(text)` metni hazır `DETECT` kalıbıyla aramadan önce
sadeleştirsin: küçük harfe çevir, `LOOKALIKE`'taki her karakteri karşılığı
olan harfle değiştir (`"1"` → `"i"` gibi) ve birden fazla boşluğu teke
indir (`" ".join(plain.split())`). Kalıp bulunursa `True`.

**Beklenen çıktı:**

```
True
True
False
```
