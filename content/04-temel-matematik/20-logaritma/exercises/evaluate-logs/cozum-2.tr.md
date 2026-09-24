**Fikir:** Deneme yapmak yerine içerideki sayıyı doğrudan **tabanın kuvveti** olarak yazabiliriz. Sonra şu kural işi bitirir:

$$
\log_b (b^k) = k
$$

Neden? $\log_b (b^k)$ "b'yi kaçıncı kuvvete çıkarırsam $b^k$ olur?" diye soruyor; cevap açıkça $k$. Logaritma ile aynı tabandaki üs birbirini siler.

**Adım 1 — $81$'i 3'ün kuvveti olarak yaz.** $81 = 9 \cdot 9 = 3 \cdot 3 \cdot 3 \cdot 3 = 3^4$.

**Adım 2 — $\frac{1}{8}$'i 2'nin kuvveti olarak yaz.** $8 = 2^3$ ve bir kuvvetin tersi negatif üs:

$$
\frac{1}{8} = \frac{1}{2^3} = 2^{-3}
$$

**Adım 3 — Kuralı uygula.**

$$
\begin{aligned}
\log_3 81 + \log_2 \tfrac{1}{8} &= \log_3 3^4 + \log_2 2^{-3} \\
&= 4 + (-3) \\
&= 1
\end{aligned}
$$

**Ne zaman işe yarar?** İçerideki sayıyı tabanın kuvveti olarak yazabildiğin her durumda bu yol en hızlısı. Yazamıyorsan (örneğin $\log_3 10$) sonuç tam sayı değildir.

**Cevap:** 1.
