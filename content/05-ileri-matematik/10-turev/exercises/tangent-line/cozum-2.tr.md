**Fikir:** Türev tablosunu kullanmadan, eğimi doğrudan tanımdan bul. $(1 + h)^3 = 1 + 3h + 3h^2 + h^3$.

**Adım 1 — Fark.**

$$
\begin{aligned}
f(1 + h) &= 1 + 3h + 3h^2 + h^3 - 2 - 2h \\
&= -1 + h + 3h^2 + h^3
\end{aligned}
$$

**Adım 2 — Eğim.** $\frac{f(1 + h) - (-1)}{h} = 1 + 3h + h^2 \to 1$.

**Adım 3 — Teğet.** $(1, -1)$'den geçen eğimi $1$ olan doğru: $y = x - 2$.

**Neden aynı sonuç?** Tablodaki $(x^3)' = 3x^2$ tam bu açılımdan geliyor: $(x + h)^3 - x^3 = 3x^2 h + 3xh^2 + h^3$, bölü $h$ ve $h \to 0$. Tablo, tanımın bir kere yapılmış hâli.

**Cevap:** $1$ ve $-2$.
