**Fikir:** Kalan teoremine göre $P(a)$, $(x - a)$'ya bölümden kalan. Sentetik bölme bu kalanı kuvvet almadan, yalnızca çarpıp toplayarak verir.

**Adım 1 — $a = 2$.** Katsayılar $2, -1, 4, -7$.

| | $2$ | $-1$ | $4$ | $-7$ |
|---|---|---|---|---|
| $a = 2$ | | $4$ | $6$ | $20$ |
| sonuç | $2$ | $3$ | $10$ | $13$ |

**Adım 2 — $a = -1$.**

| | $2$ | $-1$ | $4$ | $-7$ |
|---|---|---|---|---|
| $a = -1$ | | $-2$ | $3$ | $-7$ |
| sonuç | $2$ | $-3$ | $7$ | $-14$ |

**Adım 3 — $a = 1$.** Her adımda $1$ ile çarpmak, sayıları olduğu gibi eklemek demek: $2$, $1$, $5$, $-2$. Son sayı, katsayıların toplamı.

**Neden aynı sonuç?** Sentetik bölme, $P(x) = ((2x - 1)x + 4)x - 7$ yazımının adım adım hesabı; parantezleri açınca polinomun kendisi çıkıyor. Bu yüzden son sayı tam olarak $P(a)$.

**Cevap:** $13$, $-14$ ve $-2$.
