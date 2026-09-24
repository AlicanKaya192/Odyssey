**Ne soruluyor?** $A^{-1}$; yöntem olarak Gauss–Jordan.

**Fikir:** $A$'nın yanına $I$'yı yaz. Satır işlemleriyle sol tarafı $I$'ya çevir; aynı işlemler sağ taraftaki $I$'yı $A^{-1}$'e çevirir. Çünkü $A$'yı $I$'ya çeviren işlemler dizisi, $A^{-1}$ ile soldan çarpmakla aynı.

**Adım 1 — Başlangıç.**

$$
\left[\begin{array}{cc|cc} 1 & 2 & 1 & 0 \\ 3 & 7 & 0 & 1 \end{array}\right]
$$

**Adım 2 — 1. sütunun altını sıfırla.** $R_2 \to R_2 - 3R_1$: $(3 - 3,\ 7 - 6 \mid 0 - 3,\ 1 - 0)$.

$$
\left[\begin{array}{cc|cc} 1 & 2 & 1 & 0 \\ 0 & 1 & -3 & 1 \end{array}\right]
$$

Sol tarafın 2. pivotu zaten $1$; ölçeklemeye gerek yok.

**Adım 3 — 2. pivotun üstünü sıfırla.** $R_1 \to R_1 - 2R_2$: $(1 - 0,\ 2 - 2 \mid 1 + 6,\ 0 - 2)$.

$$
\left[\begin{array}{cc|cc} 1 & 0 & 7 & -2 \\ 0 & 1 & -3 & 1 \end{array}\right]
$$

Sol taraf $I$: sağ taraf $A^{-1}$.

$$
A^{-1} = \begin{bmatrix} 7 & -2 \\ -3 & 1 \end{bmatrix}
$$

**Sağlama:**

$$
\begin{bmatrix} 1 & 2 \\ 3 & 7 \end{bmatrix} \begin{bmatrix} 7 & -2 \\ -3 & 1 \end{bmatrix} = \begin{bmatrix} 7 - 6 & -2 + 2 \\ 21 - 21 & -6 + 7 \end{bmatrix} = I
$$

✓

**Cevap:** $A^{-1} = \begin{bmatrix} 7 & -2 \\ -3 & 1 \end{bmatrix}$.
