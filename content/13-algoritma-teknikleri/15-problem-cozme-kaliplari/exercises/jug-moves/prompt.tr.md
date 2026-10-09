`min_moves(a, b, goal)` fonksiyonunu **BFS** ile yaz: `a` ve `b` litrelik iki
boş kovayla, kovalardan birinde tam `goal` litre olması için gereken en az
hamle sayısını döndürsün; imkânsızsa `-1`.

Hamleler: birini doldur, birini boşalt, birinden ötekine taşmadan dök. Durum
`(x, y)`; uzaklıkları bir sözlükte tut.

**Beklenen çıktı:**

```
6
-1
10
```
