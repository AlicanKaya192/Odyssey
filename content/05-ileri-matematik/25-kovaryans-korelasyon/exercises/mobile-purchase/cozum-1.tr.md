**Ne soruluyor?** Ortak dağılım tablosundan kovaryans ve korelasyon.

**Fikir:** $\operatorname{Cov} = E[XY] - E[X]E[Y]$; iki değişken de Bernoulli.

**Adım 1 — $E[XY]$.** Yalnızca $(1, 1)$ hücresi katkı verir: $0{,}3$.

**Adım 2 — Kovaryans.** $E[X] = 0{,}2 + 0{,}3 = 0{,}5$, $E[Y] = 0{,}1 + 0{,}3 = 0{,}4$. $0{,}3 - 0{,}5 \cdot 0{,}4 = 0{,}1$.

**Adım 3 — Korelasyon.** $\operatorname{Var}X = 0{,}25$, $\operatorname{Var}Y = 0{,}24$. $r = \frac{0{,}1}{\sqrt{0{,}06}} \approx 0{,}408$.

**Sağlama:** Mobilde satın alma oranı $\frac{0{,}3}{0{,}5} = 0{,}6$, masaüstünde $\frac{0{,}1}{0{,}5} = 0{,}2$; mobil ile satın alma birlikte artıyor, pozitif kovaryans tutarlı ✓.

**Dikkat:** $E[XY]$'yi $E[X]E[Y] = 0{,}2$ almak bağımsızlığı varsaymaktır; o zaman kovaryans hep $0$ çıkardı.

**Cevap:** $0{,}3$; $0{,}1$; $\approx 0{,}408$.
