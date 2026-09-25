**Fikir:** Noktanın yakınında $z > y$ ($1 > -2$) ve bu küçük oynamalarla değişmez; orada $\max(y, z) = z$. Fonksiyon yerel olarak $f = xy + z$.

**Adım 1 — Yerel biçim.** $f = xy + z$.

**Adım 2 — Kısmi türevler.** $\frac{\partial f}{\partial x} = y = -2$, $\frac{\partial f}{\partial y} = x = 3$, $\frac{\partial f}{\partial z} = 1$.

**Neden aynı sonuç?** Max düğümünün "yalnızca kazanana yolla" kuralı, max'ın o noktada kazanan girdiye eşit bir fonksiyon gibi davranmasından geliyor. ReLU da aynı mantık: $\max(0, z)$, $z > 0$ iken $z$, değilken $0$.

**Cevap:** $-2$, $3$, $1$.
