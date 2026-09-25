**Fikir:** Olabilirlikleri bir ölçekte seç: $P(\text{kelime} \mid \text{spam değil}) = q$ ise $P(\text{kelime} \mid \text{spam}) = 8q$. $q$ sonunda sadeleşir.

**Adım 1 — Önsel oran.** $\frac{1}{4}$.

**Adım 2 — Birinci kelime.** $\frac{8q \cdot 0{,}2}{8q \cdot 0{,}2 + q \cdot 0{,}8} = \frac{1{,}6}{1{,}6 + 0{,}8} = \frac{2}{3}$.

**Adım 3 — İkinci kelime.** Önsel $\frac{2}{3}$, olabilirlikler $3r$ ve $r$: $\frac{3 \cdot \frac{2}{3}}{3 \cdot \frac{2}{3} + \frac{1}{3}} = \frac{2}{2 + \frac{1}{3}} = \frac{6}{7}$.

**Neden aynı sonuç?** Bayes kuralında pay ve paydadaki $q$ ile $r$ sadeleşiyor; geriye yalnızca oranları kalıyor. Oran biçimi bu sadeleşmenin önceden yapılmış hâli.

**Cevap:** $\frac{1}{4}$; $\frac{2}{3}$ ve $\frac{6}{7}$.
