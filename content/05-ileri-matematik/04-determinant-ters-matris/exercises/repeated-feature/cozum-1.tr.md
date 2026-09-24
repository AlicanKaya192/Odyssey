**Ne soruluyor?** İki veri matrisi için $X^\mathsf{T}X$'in determinantı. Sıfır çıkarsa regresyon formülündeki ters alınamaz.

**Fikir:** $X^\mathsf{T}X$'in $(i, j)$ elemanı, $X^\mathsf{T}$'nin $i$. satırı ile $X$'in $j$. sütununun nokta çarpımı. $X^\mathsf{T}$'nin satırları $X$'in sütunları olduğu için bu, **$X$'in $i$. ve $j$. sütunlarının nokta çarpımı**.

$X_1$'in sütunları $\mathbf{c}_1 = (1, 2, 3)$ ve $\mathbf{c}_2 = (2, 4, 6)$.

**Adım 1 — $X_1^\mathsf{T}X_1$.**

$$
\begin{aligned}
\mathbf{c}_1 \cdot \mathbf{c}_1 &= 1 + 4 + 9 = 14 \\
\mathbf{c}_1 \cdot \mathbf{c}_2 &= 2 + 8 + 18 = 28 \\
\mathbf{c}_2 \cdot \mathbf{c}_2 &= 4 + 16 + 36 = 56
\end{aligned}
$$

$$
X_1^\mathsf{T}X_1 = \begin{bmatrix} 14 & 28 \\ 28 & 56 \end{bmatrix}
$$

**Adım 2 — Determinantı.**

$$
14 \cdot 56 - 28 \cdot 28 = 784 - 784 = 0
$$

**Adım 3 — $X_2^\mathsf{T}X_2$.** 2. sütun artık $(2, 4, 7)$:

$$
\begin{aligned}
\mathbf{c}_1 \cdot \mathbf{c}_1 &= 14 \\
\mathbf{c}_1 \cdot \mathbf{c}_2 &= 2 + 8 + 21 = 31 \\
\mathbf{c}_2 \cdot \mathbf{c}_2 &= 4 + 16 + 49 = 69
\end{aligned}
$$

$$
X_2^\mathsf{T}X_2 = \begin{bmatrix} 14 & 31 \\ 31 & 69 \end{bmatrix}
$$

**Adım 4 — Determinantı.**

$$
14 \cdot 69 - 31 \cdot 31 = 966 - 961 = 5
$$

**Sonucu yorumla:** $X_1$'de ikinci özellik birincinin tam 2 katı; ikisi aynı bilgiyi taşıyor ve $X^\mathsf{T}X$ tekil. Formüldeki ters yok, model iki özelliğin etkisini ayıramaz. Tek bir sayının ($6 \to 7$) değişmesi determinantı $5$ yapıyor ve ters var. Ama $5$, $966$ gibi sayıların farkından çıkan küçük bir sayı: sütunlar **neredeyse** aynı doğruda ve ağırlıklar kararsız olacak.

**Cevap:** $0$ ve $5$.
