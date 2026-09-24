**Ne soruluyor?** Bir nöronun iki parametresine göre kaybın türevi ve bir öğrenme adımı.

**Fikir:** $L$, $w$'ye $\hat{y}$ ve $z$ üzerinden bağlı; zincir kuralı her halkanın türevini çarpar. Önce ileri geçişle ara değerleri bul.

**Adım 1 — İleri geçiş.** $z = 0 \cdot 2 + 0 = 0$, $\hat{y} = 0{,}5$, $L = 0{,}25$.

**Adım 2 — Halkalar.** $\frac{\partial L}{\partial \hat{y}} = 2(0{,}5 - 1) = -1$. $\frac{\partial \hat{y}}{\partial z} = 0{,}5 \cdot 0{,}5 = 0{,}25$. $\frac{\partial z}{\partial w} = x = 2$, $\frac{\partial z}{\partial b} = 1$.

**Adım 3 — Çarp.**

$$
\begin{aligned}
\frac{\partial L}{\partial w} &= (-1)(0{,}25)(2) = -0{,}5 \\
\frac{\partial L}{\partial b} &= (-1)(0{,}25)(1) = -0{,}25
\end{aligned}
$$

**Adım 4 — Adım.** $w \leftarrow 0 - 1 \cdot (-0{,}5) = 0{,}5$.

**Sağlama:** Yeni değerlerle ($w = 0{,}5$, $b = 0{,}25$): $z = 1{,}25$, $\hat{y} = \sigma(1{,}25) \approx 0{,}777$, kayıp $(0{,}777 - 1)^2 \approx 0{,}05$. $0{,}25$'ten düştü ✓.

**Dikkat:** Gradyan negatif; $w$ **artar**. Tahmin ($0{,}5$) hedefin ($1$) altında, $w$'yi artırmak tahmini yükseltiyor.

**Cevap:** $\frac{\partial L}{\partial w} = -0{,}5$, $\frac{\partial L}{\partial b} = -0{,}25$, yeni $w = 0{,}5$.
