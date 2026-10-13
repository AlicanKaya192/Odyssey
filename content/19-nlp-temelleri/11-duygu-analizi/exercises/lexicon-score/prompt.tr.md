`score(text)` metni küçük harfe çevirip `re.findall(r"[a-z']+", ...)` ile
kelimelere ayırsın; `GOOD`'daki her kelime için +1, `BAD`'deki her kelime
için −1 sayıp toplamı döndürsün.

**Beklenen çıktı:**

```
1
-2
0
0
```
