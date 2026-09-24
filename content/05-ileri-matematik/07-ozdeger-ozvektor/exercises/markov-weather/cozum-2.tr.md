**Fikir:** Uzun vadede güneşli günlerin payı $s$ olsun (yağmurluların $1 - s$). Bir günden ötekine güneşli günlerin payı değişmiyorsa, yarın güneşli olma olasılığı da $s$ olmalı. Bu tek denklem yeter; özvektörü hiç yazmadan.

**Adım 1 — Yarının güneşli olma olasılığı.** Bugün güneşliyse ($s$ olasılıkla) yarın $0.9$ ile, yağmurluysa ($1 - s$ olasılıkla) $0.5$ ile güneşli:

$$
0.9\,s + 0.5\,(1 - s)
$$

**Adım 2 — Dengeye eşitle.**

$$
\begin{aligned}
0.9\,s + 0.5\,(1 - s) &= s \\
0.9\,s + 0.5 - 0.5\,s &= s \\
0.5 &= s - 0.4\,s \\
0.5 &= 0.6\,s \\
s &= \frac{5}{6}
\end{aligned}
$$

**Adım 3 — Öteki özdeğer, determinanttan.** Özdeğerlerin çarpımı determinant:

$$
\det M = 0.9 \cdot 0.5 - 0.5 \cdot 0.1 = 0.45 - 0.05 = 0.4
$$

Bir özdeğer $1$ olduğuna göre öteki $0.4$.

**Neden aynı sonuç?** Denge denklemi, $M\mathbf{p} = \mathbf{p}$'nin ilk satırını $\mathbf{p} = (s, 1 - s)$ koyarak yazmak. Toplamın $1$ olması şartı en baştan yerleştirildiği için ayrıca bölmek gerekmedi.

**Neden 1 hep bir özdeğer?** Her sütunun toplamı $1$ (bir günden sonra mutlaka bir hava olur). Bu, $M^\mathsf{T}(1, 1) = (1, 1)$ demek; $M^\mathsf{T}$ ile $M$'nin özdeğerleri aynı olduğu için $1$, $M$'nin de özdeğeri.

**Cevap:** $\tfrac{5}{6}$ ve $0.4$.
