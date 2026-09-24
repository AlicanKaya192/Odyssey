**Ne soruluyor?** İki bilinmeyenli iki denklem. Matris diliyle $A\mathbf{x} = \mathbf{b}$ ve çözüm $\mathbf{x} = A^{-1}\mathbf{b}$.

**Fikir:** Sayılarda $3x = 6$'yı 3'e bölerek çözeriz. Matrislerde bölme yok; onun yerine iki tarafı soldan $A^{-1}$ ile çarparız: $A^{-1}A\mathbf{x} = \mathbf{x}$.

**Adım 1 — Matris biçimi.** Katsayılar satır satır $A$'ya, sağ taraflar $\mathbf{b}$'ye:

$$
\begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 4 \\ 11 \end{bmatrix}
$$

**Adım 2 — Determinant.**

$$
\det A = 2 \cdot 3 - 1 \cdot 5 = 6 - 5 = 1
$$

Sıfır değil: sistemin tam bir çözümü var.

**Adım 3 — Ters.** Yer değiştir, işaret çevir, $1$'e böl:

$$
A^{-1} = \begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix}
$$

**Adım 4 — $\mathbf{x} = A^{-1}\mathbf{b}$.** Satır çarpı vektör:

$$
\begin{aligned}
\begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix} \begin{bmatrix} 4 \\ 11 \end{bmatrix} &= \begin{bmatrix} 3 \cdot 4 - 1 \cdot 11 \\ -5 \cdot 4 + 2 \cdot 11 \end{bmatrix} \\
&= \begin{bmatrix} 12 - 11 \\ -20 + 22 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}
\end{aligned}
$$

**Sağlama:** Orijinal denklemlere koy: $2 \cdot 1 + 2 = 4$ ✓ ve $5 \cdot 1 + 3 \cdot 2 = 11$ ✓.

**Dikkat:** $A^{-1}$ **soldan** çarpılır. $\mathbf{b}$'yi soldan, $A^{-1}$'i sağdan yazmak ($\mathbf{b}A^{-1}$) tanımsız.

**Cevap:** $x = 1$, $y = 2$.
