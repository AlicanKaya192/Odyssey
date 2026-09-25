**Fikir:** İlk iki cevabın aynı çıkması tesadüf değil. Softmax'in payını ve paydasını $e^{z_1}$'e bölersek sigmoid ortaya çıkar.

**Adım 1 — Böl.**

$$
\begin{aligned}
p_1 &= \frac{e^{z_1}}{e^{z_1} + e^{z_2}} = \frac{1}{1 + \frac{e^{z_2}}{e^{z_1}}} \\
&= \frac{1}{1 + e^{-(z_1 - z_2)}} = \sigma(z_1 - z_2)
\end{aligned}
$$

**Adım 2 — Sayılar.** $\frac{e^{z_2}}{e^{z_1}} = \frac{1}{3}$, yani iki soru da $\frac{1}{1 + 1/3} = \frac{3}{4}$.

**Adım 3 — Üç sınıf.** Burada sigmoid kısa yolu yok; payda $12 + 4 + 4 = 20$, $p_1 = \frac{3}{5}$.

**Neden aynı sonuç?** İki sınıfta yalnızca puanların **farkı** önemli: $z_1$ ile $z_2$'ye aynı sayı eklense $e^{z}$'lerin ikisi de aynı çarpanla büyür ve oran değişmez. Lojistik regresyon (sigmoid) bu yüzden iki sınıflı softmax'in ta kendisi.

**Cevap:** $\frac{3}{4}$, $\frac{3}{4}$ ve $\frac{3}{5}$.
