**Ne soruluyor?** Bir katsayı, polinomun en küçük kökü ve bir bölmenin kalanı.

**Fikir:** Çarpan teoremi $P(2) = 0$ der; bu $k$'yi verir. Sonra polinom çarpanlarına ayrılır, kalan için de kalan teoremi kullanılır.

**Adım 1 — $k$.**

$$
\begin{aligned}
P(2) &= 8 + 4k - 8 - 12 = 4k - 12 \\
4k - 12 &= 0 \quad \Rightarrow \quad k = 3
\end{aligned}
$$

**Adım 2 — Çarpanlar.** $P(x) = x^3 + 3x^2 - 4x - 12$. İki iki grupla:

$$
\begin{aligned}
x^3 + 3x^2 - 4x - 12 &= x^2(x + 3) - 4(x + 3) \\
&= (x + 3)(x^2 - 4) \\
&= (x + 3)(x - 2)(x + 2)
\end{aligned}
$$

Kökler $-3$, $-2$, $2$; en küçüğü $-3$.

**Adım 3 — Kalan.** $(x + 1)$ için $a = -1$: $P(-1) = -1 + 3 + 4 - 12 = -6$.

**Sağlama:** $P(-3) = -27 + 27 + 12 - 12 = 0$ ✓, $P(-2) = -8 + 12 + 8 - 12 = 0$ ✓.

**Dikkat:** $(x + 1)$'e bölümden kalan $P(1)$ değil $P(-1)$; $P(1) = -12$ yanlış cevap olurdu.

**Cevap:** $k = 3$, en küçük kök $-3$, kalan $-6$.
