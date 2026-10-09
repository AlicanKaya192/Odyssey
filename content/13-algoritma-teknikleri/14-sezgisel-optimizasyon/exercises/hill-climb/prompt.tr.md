`hill_climb(x, step)` fonksiyonunu yaz: `f` hazır. Her adımda `x - step` ve
`x + step`'ten `f`'i küçük olana bak (`min(..., key=f)`); `x`'ten daha iyi
değilse dur ve `round(x, 2)` döndür, iyiyse oraya geç.

**Beklenen çıktı:**

```
-20 -20
-5 -7.7
0 -1.5
4 4.6
18 16.9
```
