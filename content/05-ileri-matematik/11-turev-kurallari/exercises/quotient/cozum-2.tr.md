**Fikir:** Bölüm kuralını hiç kullanmadan: $f(x) = x \cdot (x^2 + 1)^{-1}$ yaz; çarpım kuralı, ikinci çarpanda zincir kuralı.

**Adım 1 — İkinci çarpanın türevi.** $\big((x^2 + 1)^{-1}\big)' = -(x^2 + 1)^{-2} \cdot 2x$.

**Adım 2 — Çarpım kuralı.**

$$
\begin{aligned}
f'(x) &= 1 \cdot (x^2 + 1)^{-1} + x \cdot \big(-2x (x^2 + 1)^{-2}\big) \\
&= \frac{(x^2 + 1) - 2x^2}{(x^2 + 1)^2} = \frac{1 - x^2}{(x^2 + 1)^2}
\end{aligned}
$$

**Adım 3 — Değerler.** $f'(2) = -\frac{3}{25}$; pay $1 - x^2 = 0$, $x = 1$.

**Neden aynı sonuç?** Bölüm kuralı zaten bu iki kuralın birleşiminden türetiliyor; ortak paydaya getirince aynı kesir çıkıyor. Kuralı unutursan bu yol her zaman elinde.

**Cevap:** $-\frac{3}{25}$ ve $1$.
