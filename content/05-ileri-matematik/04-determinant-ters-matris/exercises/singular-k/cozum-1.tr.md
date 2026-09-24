**Ne soruluyor?** $A$'nın tersinin olmadığı $k$ değerleri. Ters ancak determinant sıfırdan farklıysa var; o yüzden determinantın **sıfır** olduğu yerleri arıyoruz.

**Fikir:** $\det A$'yı $k$ cinsinden yaz, sıfıra eşitle, çıkan denklemi çöz.

**Adım 1 — Determinant.** $ad - bc$ ile:

$$
\begin{aligned}
\det A &= k \cdot (k + 1) - 4 \cdot 3 \\
&= k^2 + k - 12
\end{aligned}
$$

**Adım 2 — Sıfıra eşitle.**

$$
k^2 + k - 12 = 0
$$

**Adım 3 — Çarpanlarına ayır.** Çarpımı $-12$, toplamı $+1$ olan iki sayı: $4$ ve $-3$ ($4 \cdot (-3) = -12$, $4 + (-3) = 1$).

$$
(k + 4)(k - 3) = 0
$$

Bir çarpım ancak çarpanlardan biri sıfırsa sıfır: $k = 3$ ya da $k = -4$.

**Sağlama:** $k = 3$ için $\begin{bmatrix} 3 & 4 \\ 3 & 4 \end{bmatrix}$, determinant $12 - 12 = 0$ ✓. $k = -4$ için $\begin{bmatrix} -4 & 4 \\ 3 & -3 \end{bmatrix}$, determinant $12 - 12 = 0$ ✓.

**Sonucu yorumla:** Bu iki değer dışındaki **her** $k$ için $A$ tersinir.

**Cevap:** pozitif $k = 3$, negatif $k = -4$.
