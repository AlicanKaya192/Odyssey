**Ne soruluyor?** Σ ile yazılmış üç toplamın değeri.

**Fikir:** Toplam kuralları ve bilinen formüller: $\sum_{i=1}^{n} i = \frac{n(n + 1)}{2}$, geometrik seri $a_1 \frac{1 - r^n}{1 - r}$.

**Adım 1 — Birinci.**

$$
\begin{aligned}
\sum_{i=1}^{20} (2i - 3) &= 2 \sum_{i=1}^{20} i - \sum_{i=1}^{20} 3 \\
&= 2 \cdot 210 - 20 \cdot 3 = 360
\end{aligned}
$$

**Adım 2 — İkinci.** Terimler $3, 6, 12, \dots, 96$: $a_1 = 3$, $r = 2$, $6$ terim.

$$
3 \cdot \frac{1 - 2^6}{1 - 2} = 3 \cdot 63 = 189
$$

**Adım 3 — Üçüncü.** $5$'ten başlayan toplamı $1$'den başlayanların farkı olarak yaz:

$$
\sum_{i=5}^{12} i = \sum_{i=1}^{12} i - \sum_{i=1}^{4} i = 78 - 10 = 68
$$

**Sağlama:** Üçüncüde $8$ terim var ($12 - 5 + 1$), ortalamaları $\frac{5 + 12}{2} = 8{,}5$; $8 \cdot 8{,}5 = 68$ ✓.

**Dikkat:** $\sum 3$'ü $3$ saymak yaygın hata; sabit, terim sayısı kadar eklenir: $20 \cdot 3 = 60$.

**Cevap:** $360$, $189$, $68$.
