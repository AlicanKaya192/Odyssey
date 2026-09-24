**Fikir:** Aynı çarpıma sütun gözüyle bak. $X\mathbf{w}$, $X$'in sütunlarının $\mathbf{w}$'deki ağırlıklarla toplamı. $X$'in her sütunu bir özellik (alan, oda, yaş) olduğu için her sütun çarpımı, o özelliğin **üç evin fiyatına katkısını** tek seferde veriyor.

**Adım 1 — Alanın payı.** Alan sütununu ağırlığı $100$ ile çarp:

$$
100 \begin{bmatrix} 1.2 \\ 0.8 \\ 1.5 \end{bmatrix} = \begin{bmatrix} 120 \\ 80 \\ 150 \end{bmatrix}
$$

**Adım 2 — Odanın payı.** Oda sütununu $20$ ile çarp:

$$
20 \begin{bmatrix} 3 \\ 2 \\ 4 \end{bmatrix} = \begin{bmatrix} 60 \\ 40 \\ 80 \end{bmatrix}
$$

**Adım 3 — Yaşın payı.** Yaş sütununu $-2$ ile çarp; yaşlı ev daha çok düşer:

$$
-2 \begin{bmatrix} 10 \\ 25 \\ 5 \end{bmatrix} = \begin{bmatrix} -20 \\ -50 \\ -10 \end{bmatrix}
$$

**Adım 4 — Payları ve $b$'yi topla.** Her satır kendi içinde toplanıyor:

$$
\begin{aligned}
\hat{y}_1 &= 120 + 60 - 20 + 10 = 170 \\
\hat{y}_2 &= 80 + 40 - 50 + 10 = 80 \\
\hat{y}_3 &= 150 + 80 - 10 + 10 = 230
\end{aligned}
$$

**Neden aynı sonuç?** Birinci yolda aynı sayıları satır satır topladık, burada sütun sütun. Toplamanın sırası sonucu değiştirmez.

**Bu bakışın faydası:** 2. evin neden ucuz çıktığı hemen görünüyor: yaşının payı $-50$, üç ev içinde en büyük düşüş. Bir modelin tahminini özelliklerin katkılarına ayırıp açıklamak tam bu fikre dayanıyor.

**Cevap:** $170$, $80$, $230$.
