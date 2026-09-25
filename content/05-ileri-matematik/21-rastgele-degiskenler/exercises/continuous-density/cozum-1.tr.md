**Ne soruluyor?** Bir yoğunluğun normalleştirme sabiti, beklenen değeri ve bir aralığın olasılığı.

**Fikir:** Toplam alan $1$ olmalı; beklenen değer $\int x f(x) dx$; olasılık alan.

**Adım 1 — $c$.**

$$
\int_0^2 (2x - x^2) \, dx = \Big[x^2 - \tfrac{x^3}{3}\Big]_0^2 = 4 - \tfrac{8}{3} = \tfrac{4}{3}
$$

$c \cdot \frac{4}{3} = 1$, $c = \frac{3}{4}$.

**Adım 2 — $E[X]$.**

$$
\begin{aligned}
E[X] &= \tfrac{3}{4} \int_0^2 (2x^2 - x^3) \, dx = \tfrac{3}{4} \Big[\tfrac{2x^3}{3} - \tfrac{x^4}{4}\Big]_0^2 \\
&= \tfrac{3}{4} \left( \tfrac{16}{3} - 4 \right) = \tfrac{3}{4} \cdot \tfrac{4}{3} = 1
\end{aligned}
$$

**Adım 3 — Olasılık.**

$$
\begin{aligned}
P(X \leq 0{,}5) &= \tfrac{3}{4} \Big[x^2 - \tfrac{x^3}{3}\Big]_0^{0{,}5} \\
&= \tfrac{3}{4} \left( \tfrac{1}{4} - \tfrac{1}{24} \right) = \tfrac{3}{4} \cdot \tfrac{5}{24} = \tfrac{5}{32}
\end{aligned}
$$

**Sağlama:** $\frac{5}{32} \approx 0{,}156$; aralık $[0, 2]$'nin dörtte biri ama yoğunluk kenarda küçük, olasılık $0{,}25$'ten az olmalı ✓.

**Dikkat:** $c$'yi bulmadan olasılık hesaplamak; yoğunluğun alanı $1$ olmadan sonuç olasılık değildir.

**Cevap:** $c = \frac{3}{4}$, $E[X] = 1$, $P = \frac{5}{32}$.
