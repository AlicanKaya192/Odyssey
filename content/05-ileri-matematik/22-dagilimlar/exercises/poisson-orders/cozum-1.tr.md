**Ne soruluyor?** Sabit hızda gelen olayların sayısıyla ilgili üç olasılık.

**Fikir:** Bağımsız ve sabit ortalama hızda gelen olaylar: Poisson$(\lambda = 4)$.

**Adım 1 — Hiç yok.** $e^{-4} \approx 0{,}0183$.

**Adım 2 — Tam $4$.**

$$
\frac{e^{-4} \, 4^4}{4!} = \frac{256}{24} e^{-4} \approx 10{,}667 \cdot 0{,}0183 \approx 0{,}1954
$$

**Adım 3 — En az $2$.** $P(1) = 4e^{-4} \approx 0{,}0733$. $1 - 0{,}0183 - 0{,}0733 = 1 - 5e^{-4} \approx 0{,}9084$.

**Sağlama:** Poisson'da ortalama $4$ iken $P(3) = P(4) \approx 0{,}195$; iki komşu değerin eşit çıkması $\lambda$ tam sayı olduğunda olur ✓.

**Dikkat:** "En az $2$"de yalnızca $P(0)$'ı çıkarmak "en az $1$"i verir.

**Cevap:** $\approx 0{,}0183$; $\approx 0{,}1954$; $\approx 0{,}9084$.
