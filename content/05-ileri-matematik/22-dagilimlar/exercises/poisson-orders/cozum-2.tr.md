**Fikir:** Poisson'da ardışık olasılıkların oranı basit: $\frac{P(k)}{P(k - 1)} = \frac{\lambda}{k}$. $P(0)$'dan başlayıp çarparak ilerle.

**Adım 1 — $P(0)$.** $e^{-4} \approx 0{,}01832$.

**Adım 2 — Yürü.** $P(1) = P(0) \cdot 4 = 0{,}07326$; $P(2) = P(1) \cdot 2 = 0{,}14653$; $P(3) = P(2) \cdot \frac{4}{3} = 0{,}19537$; $P(4) = P(3) \cdot 1 = 0{,}19537$.

**Adım 3 — En az $2$.** $1 - 0{,}01832 - 0{,}07326 = 0{,}90842$.

**Neden aynı sonuç?** $\frac{\lambda^k / k!}{\lambda^{k-1} / (k-1)!} = \frac{\lambda}{k}$; formül bu çarpanların birikmiş hâli. $k = \lambda$'da oran $1$ olduğu için $P(3) = P(4)$.

**Cevap:** $0{,}0183$; $0{,}1954$ ve $0{,}9084$.
