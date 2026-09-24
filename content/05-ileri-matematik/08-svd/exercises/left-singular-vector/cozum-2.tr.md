**Fikir:** $\mathbf{v}_i$'ler $A^\mathsf{T}A$'nın özvektörleri olduğu gibi, $\mathbf{u}_i$'ler de $AA^\mathsf{T}$'nin özvektörleri: $AA^\mathsf{T} = U(\Sigma\Sigma^\mathsf{T})U^\mathsf{T}$. Özdeğerleri yine $\sigma_i^2$. $\mathbf{v}_1$'i kullanmadan $\mathbf{u}_1$'i doğrudan bulabiliriz.

**Adım 1 — $AA^\mathsf{T}$.** Bu kez $A$'nın **satırlarının** nokta çarpımları:

$$
\begin{aligned}
AA^\mathsf{T} &= \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix} \begin{bmatrix} 3 & 4 \\ 0 & 5 \end{bmatrix} \\
&= \begin{bmatrix} 9 & 12 \\ 12 & 41 \end{bmatrix}
\end{aligned}
$$

İz $50$, determinant $369 - 144 = 225$: özdeğerler yine $45$ ve $5$ ✓.

**Adım 2 — $\lambda = 45$ için özvektör.**

$$
AA^\mathsf{T} - 45I = \begin{bmatrix} -36 & 12 \\ 12 & -4 \end{bmatrix}
$$

İlk satır: $-36x + 12y = 0$, yani $y = 3x$. Özvektör $(1, 3)$.

**Adım 3 — Birim uzunluğa indir.** $\|(1, 3)\| = \sqrt{10}$:

$$
\mathbf{u}_1 = \frac{1}{\sqrt{10}}(1, 3) \approx (0.32,\ 0.95)
$$

**Dikkat:** Özvektörün işareti serbest: $-(1, 3)$ de bir özvektör. SVD'de $\mathbf{u}_i$'nin işareti $A\mathbf{v}_i = \sigma_i\mathbf{u}_i$ ile $\mathbf{v}_i$'ye bağlanıyor; soru "ikisi de pozitif" dediği için pozitif olanı seçtik.

**Cevap:** $(0.32,\ 0.95)$.
