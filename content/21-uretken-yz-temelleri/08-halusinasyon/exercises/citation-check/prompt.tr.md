`check_citations(answer, sources)` cevabı `". "` ile cümlelere bölsün. Her
cümlede `[n]` biçiminde bir kaynak numarası arasın (`n` 1'den başlar).
Cümle geçerliyse `True`: numara var, `1 <= n <= len(sources)` ve cümledeki
bütün sayılar (`r"\d+"`; numaranın kendisi hariç) `sources[n - 1]` içinde
sayı olarak geçiyor. Döndür: cümle başına `True`/`False` listesi.

**Beklenen çıktı:**

```
[True, False, False]
```
