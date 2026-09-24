**Ne soruluyor?** $B$'nin yönünü değiştirmediği vektörlerin uzama çarpanları.

**Fikir:** $B\mathbf{v} = \lambda\mathbf{v}$'nin sıfır olmayan bir çözümü, ancak $B - \lambda I$ tekilse vardır: $\det(B - \lambda I) = 0$.

**Adım 1 — $B - \lambda I$.** $\lambda$ yalnızca köşegenden çıkar:

$$
B - \lambda I = \begin{bmatrix} 4 - \lambda & 1 \\ 2 & 3 - \lambda \end{bmatrix}
$$

**Adım 2 — Determinant.**

$$
\begin{aligned}
\det(B - \lambda I) &= (4 - \lambda)(3 - \lambda) - 1 \cdot 2 \\
&= 12 - 7\lambda + \lambda^2 - 2 \\
&= \lambda^2 - 7\lambda + 10
\end{aligned}
$$

**Adım 3 — Sıfıra eşitle ve çarpanlarına ayır.** Çarpımı $10$, toplamı $-7$ olan iki sayı: $-2$ ve $-5$.

$$
\lambda^2 - 7\lambda + 10 = (\lambda - 2)(\lambda - 5) = 0
$$

Özdeğerler $\lambda = 2$ ve $\lambda = 5$.

**Sağlama:** Toplam $2 + 5 = 7 = 4 + 3$ (iz) ✓; çarpım $2 \cdot 5 = 10 = \det B$ ✓.

**Dikkat:** Köşegen elemanlar ($4$ ve $3$) özdeğer **değil**. Bu yalnızca üçgen matrislerde doğru; burada köşegen dışındaki $1$ ve $2$ de sonucu etkiliyor.

**Cevap:** $2$ ve $5$.
