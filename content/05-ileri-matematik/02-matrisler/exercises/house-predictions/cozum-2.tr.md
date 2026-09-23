Sütun bakışıyla $X\mathbf{w}$, her özellik sütununun kendi ağırlığıyla çarpılıp toplanması. Her sütun, o özelliğin **bütün evlerin fiyatına katkısını** tek seferde veriyor:

**Alanın payı:**

$$
100 \begin{bmatrix} 1.2 \\ 0.8 \\ 1.5 \end{bmatrix} = \begin{bmatrix} 120 \\ 80 \\ 150 \end{bmatrix}
$$

**Odanın payı:**

$$
20 \begin{bmatrix} 3 \\ 2 \\ 4 \end{bmatrix} = \begin{bmatrix} 60 \\ 40 \\ 80 \end{bmatrix}
$$

**Yaşın payı:**

$$
-2 \begin{bmatrix} 10 \\ 25 \\ 5 \end{bmatrix} = \begin{bmatrix} -20 \\ -50 \\ -10 \end{bmatrix}
$$

**Hepsini ve $b = 10$'u topla:**

$$
\hat{\mathbf{y}} = \begin{bmatrix} 120 + 60 - 20 + 10 \\ 80 + 40 - 50 + 10 \\ 150 + 80 - 10 + 10 \end{bmatrix} = \begin{bmatrix} 170 \\ 80 \\ 230 \end{bmatrix}
$$

Bu bakışın faydası: 2. evin ucuz çıkmasının sebebi hemen görünüyor, yaşının payı $-50$. Bir modelin tahminini özelliklere ayırıp açıklamak bu fikre dayanıyor.

**Cevap: $170$, $80$, $230$**
