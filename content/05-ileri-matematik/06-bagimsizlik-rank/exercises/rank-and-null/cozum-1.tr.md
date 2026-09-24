**Ne soruluyor?** Kaç bağımsız sütun (rank) olduğu ve $A$'nın sıfıra götürdüğü vektörlerden biri.

**Fikir:** Rank, elemeden sonraki pivot sayısı. Pivotsuz sütunlar serbest değişken; onlara değer verince çekirdekteki vektörler çıkıyor.

**Adım 1 — 1. sütunu temizle.** $R_2 \to R_2 - 2R_1$, $R_3 \to R_3 - R_1$:

$$
\begin{bmatrix} 1 & 2 & 3 \\ 0 & 0 & 0 \\ 0 & -1 & -2 \end{bmatrix}
$$

2. satır tamamen sıfırlandı: o satır 1. satırın 2 katıymış.

**Adım 2 — Sıfır satırı alta al.** $R_2 \leftrightarrow R_3$:

$$
\begin{bmatrix} 1 & 2 & 3 \\ 0 & -1 & -2 \\ 0 & 0 & 0 \end{bmatrix}
$$

**Adım 3 — Pivotları say.** 1. ve 2. sütunda pivot var, 3.'de yok: $\operatorname{rank} A = 2$.

**Adım 4 — Çekirdek.** Basamak biçimi iki denklem söylüyor:

$$
\begin{aligned}
x + 2y + 3z &= 0 \\
-y - 2z &= 0
\end{aligned}
$$

$z$ serbest. $z = 1$ koy: ikinci denklemden $y = -2$; birinciden $x = -2y - 3z = 4 - 3 = 1$.

**Sağlama:** $A(1, -2, 1)$:

$$
\begin{aligned}
1 - 4 + 3 &= 0 \\
2 - 8 + 6 &= 0 \\
1 - 2 + 1 &= 0
\end{aligned}
$$

✓

**Sonucu yorumla:** Rank–sıfırlık: $2 + 1 = 3$ sütun. Çekirdek $t\,(1, -2, 1)$ doğrusu; 1. sütun $- 2 \cdot$ 2. sütun $+$ 3. sütun $= \mathbf{0}$, yani sütunlar arasındaki bağımlılık tam olarak bu vektör.

**Cevap:** $\operatorname{rank} A = 2$; $x = 1$, $y = -2$.
