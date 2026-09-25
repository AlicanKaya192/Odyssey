**Fikir:** $\text{kayıp} = -\ln p$ ($y = 1$). $\frac{\partial\,\text{kayıp}}{\partial w} = \frac{d\,\text{kayıp}}{dp} \cdot \frac{dp}{dz} \cdot \frac{\partial z}{\partial w}$.

**Adım 1 — $p$.** $z = 0{,}5$, $p \approx 0{,}622$.

**Adım 2 — Halkalar.** $\frac{d\,\text{kayıp}}{dp} = -\frac{1}{p} \approx -1{,}607$; $\frac{dp}{dz} = p(1 - p) \approx 0{,}235$; $\frac{\partial z}{\partial w} = x = 2$. Çarpım $\approx -1{,}607 \cdot 0{,}235 \cdot 2 \approx -0{,}755$.

**Adım 3 — Güncelleme.** $0{,}5 + 0{,}0755 = 0{,}5755$.

**Neden aynı sonuç?** $-\frac{1}{p} \cdot p(1 - p) = -(1 - p) = p - 1 = p - y$; sigmoidin türevindeki $p$, logaritmanın türevindeki $\frac{1}{p}$ ile sadeleşiyor. Kısa formül bu sadeleşmenin sonucu.

**Cevap:** $0{,}622$; $-0{,}755$ ve $0{,}5755$.
