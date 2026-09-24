**Fikir:** Genel yöntemi uygulayalım: $A^\mathsf{T}A$'nın özdeğerlerinin karekökleri.

**Adım 1 — $A^\mathsf{T}A$.**

$$
\begin{aligned}
A^\mathsf{T}A &= \begin{bmatrix} 2 & 1 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} 2 & 2 \\ 1 & 1 \end{bmatrix} \\
&= \begin{bmatrix} 5 & 5 \\ 5 & 5 \end{bmatrix}
\end{aligned}
$$

**Adım 2 — Özdeğerler.** İz $10$, determinant $25 - 25 = 0$:

$$
\lambda^2 - 10\lambda = \lambda(\lambda - 10) = 0
$$

Özdeğerler $10$ ve $0$.

**Adım 3 — Karekök.** $\sigma_1 = \sqrt{10} \approx 3.16$, $\sigma_2 = 0$.

**Adım 4 — Sağ tekil vektör.** $A^\mathsf{T}A - 10I = \begin{bmatrix} -5 & 5 \\ 5 & -5 \end{bmatrix}$: $y = x$, $\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(1, 1)$. Birinci yoldaki $\mathbf{b}$'nin yönüyle aynı ✓.

**Neden aynı sonuç?** $A = \mathbf{a}\mathbf{b}^\mathsf{T}$ ise $A^\mathsf{T}A = \mathbf{b}\,(\mathbf{a}^\mathsf{T}\mathbf{a})\,\mathbf{b}^\mathsf{T} = \|\mathbf{a}\|^2\,\mathbf{b}\mathbf{b}^\mathsf{T}$. Bunun sıfır olmayan tek özdeğeri $\|\mathbf{a}\|^2\|\mathbf{b}\|^2 = 5 \cdot 2 = 10$.

**Cevap:** $3.16$ ve $0$.
