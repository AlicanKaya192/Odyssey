**Fikir:** Kosinüs formülündeki bölmeyi baştan yapabiliriz. Her vektörü önce birim vektöre çevirirsek (uzunluğu 1 olur), kosinüs benzerliği düz bir nokta çarpımına dönüşür, çünkü paydadaki uzunluklar $1 \cdot 1 = 1$ olur. Arama sistemleri çoğu zaman tam böyle çalışır.

**Adım 1 — Uzunlukları bul.** Birinci yoldaki gibi: $\|\mathbf{q}\| = \sqrt{2}$, $\|D_1\| = 3$, $\|D_2\| = 10$.

**Adım 2 — Birim vektörler.** Her bileşeni vektörün uzunluğuna böl ($1/\sqrt{2} \approx 0.707$):

$$
\begin{aligned}
\hat{\mathbf{q}} &= \frac{(1,\ 1,\ 0)}{\sqrt{2}} \approx (0.707,\ 0.707,\ 0) \\
\hat{D}_1 &= \frac{(2,\ 2,\ 1)}{3} \approx (0.667,\ 0.667,\ 0.333) \\
\hat{D}_2 &= \frac{(0,\ 6,\ 8)}{10} = (0,\ 0.6,\ 0.8)
\end{aligned}
$$

**Adım 3 — Nokta çarpımları.** Artık kosinüs benzerliği yalnızca çarp ve topla:

$$
\begin{aligned}
\hat{\mathbf{q}} \cdot \hat{D}_1 &\approx 0.707 \cdot 0.667 + 0.707 \cdot 0.667 + 0 \\
&\approx 0.472 + 0.472 \approx 0.94
\end{aligned}
$$

$$
\begin{aligned}
\hat{\mathbf{q}} \cdot \hat{D}_2 &\approx 0.707 \cdot 0 + 0.707 \cdot 0.6 + 0 \cdot 0.8 \\
&\approx 0.42
\end{aligned}
$$

**Neden bu düzen?** Milyonlarca belgede büyük kazanç: belgeler bir kez normalleştirilip saklanır, her aramada yalnızca sorgu normalleştirilir ve geriye çarp-topla kalır.

**Cevap:** $0.94$ ve $0.42$; $D_1$ daha benzer.
