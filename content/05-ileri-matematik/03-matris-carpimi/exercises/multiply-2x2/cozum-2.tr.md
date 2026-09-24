**Fikir:** $AB$'nin her sütunu, $A$ ile $B$'nin o sütununun çarpımı. Yani iki ayrı matris–vektör çarpımı yapacağız. Matris–vektör çarpımında da sütun bakışını kullanabiliriz: $A\mathbf{b}$, $A$'nın sütunlarının $\mathbf{b}$'nin bileşenleriyle ağırlıklı toplamı.

$A$'nın sütunları $\mathbf{a}_1 = (2, 3)$ ve $\mathbf{a}_2 = (-1, 4)$.

**Adım 1 — $C$'nin 1. sütunu: $A\,(1, 0)$.** Ağırlıklar $1$ ve $0$: yalnızca $A$'nın 1. sütunu kalıyor.

$$
1 \begin{bmatrix} 2 \\ 3 \end{bmatrix} + 0 \begin{bmatrix} -1 \\ 4 \end{bmatrix} = \begin{bmatrix} 2 \\ 3 \end{bmatrix}
$$

**Adım 2 — $C$'nin 2. sütunu: $A\,(2, -3)$.** $A$'nın 1. sütununun 2 katı ile 2. sütununun $-3$ katını topla:

$$
\begin{aligned}
2 \begin{bmatrix} 2 \\ 3 \end{bmatrix} - 3 \begin{bmatrix} -1 \\ 4 \end{bmatrix} &= \begin{bmatrix} 4 \\ 6 \end{bmatrix} + \begin{bmatrix} 3 \\ -12 \end{bmatrix} \\
&= \begin{bmatrix} 7 \\ -6 \end{bmatrix}
\end{aligned}
$$

**Adım 3 — Sütunları yan yana koy.**

$$
C = \begin{bmatrix} 2 & 7 \\ 3 & -6 \end{bmatrix}
$$

**Neden aynı sonuç?** Birinci yolda her elemanı ayrı hesapladık; burada bir sütunun iki elemanını birlikte ürettik. Toplanan sayılar aynı, yalnızca gruplama farklı. Bu bakış, $B$'nin $1, 0$ gibi basit sütunları olduğunda hesabı çok kısaltıyor.

**Cevap:** $2$, $7$, $3$, $-6$.
