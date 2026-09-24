**Fikir:** Tersi hiç yazmadan, yalnızca determinantlarla da çözülebilir (**Cramer kuralı**). Bir bilinmeyeni bulmak için $A$'da o bilinmeyenin sütununu $\mathbf{b}$ ile değiştir, yeni determinantı $\det A$'ya böl:

$$
x = \frac{\det A_x}{\det A}
\qquad
y = \frac{\det A_y}{\det A}
$$

Neden işe yarar? $\mathbf{x} = A^{-1}\mathbf{b}$'yi $2 \times 2$ ters formülüyle açınca payda $\det A$, payda da tam bu küçük determinantlar çıkıyor.

**Adım 1 — $\det A$.** $2 \cdot 3 - 1 \cdot 5 = 1$.

**Adım 2 — $x$ için.** 1. sütunu ($x$'in katsayıları $2, 5$) $\mathbf{b} = (4, 11)$ ile değiştir:

$$
\det A_x = \begin{vmatrix} 4 & 1 \\ 11 & 3 \end{vmatrix} = 12 - 11 = 1
$$

$$
x = \frac{1}{1} = 1
$$

**Adım 3 — $y$ için.** 2. sütunu ($1, 3$) $\mathbf{b}$ ile değiştir:

$$
\det A_y = \begin{vmatrix} 2 & 4 \\ 5 & 11 \end{vmatrix} = 22 - 20 = 2
$$

$$
y = \frac{2}{1} = 2
$$

**Ne zaman kullanılır?** İki ya da üç bilinmeyenli küçük sistemlerde, özellikle yalnızca **bir** bilinmeyen sorulduğunda hızlı. Büyük sistemlerde çok yavaş; orada Gauss eleme kullanılır.

**Cevap:** $x = 1$, $y = 2$.
