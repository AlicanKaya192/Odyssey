`edit_distance(a, b)` fonksiyonunu yaz: `a`'yı `b`'ye çevirmek için gereken
en az **ekleme, silme, değiştirme** sayısını döndürsün. Sonra
`suggest(word, vocabulary)` sözlükteki en yakın kelimeyi döndürsün (eşitlikte
listede önce geleni; `min(..., key=...)` bunu zaten yapar).

`dp[i][0] = i`, `dp[0][j] = j`; her hücre üstten + 1, soldan + 1, çaprazdan
+ (harfler farklıysa 1) seçeneklerinin en küçüğü.

**Beklenen çıktı:**

```
3
pyhton -> python
nmupy -> numpy
matplotib -> matplotlib
```
