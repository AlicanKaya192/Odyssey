**Fikir:** Standart sapma yerine varyansla çalış; bağımsız toplamda varyanslar toplanır.

**Adım 1 — Varyans.** Tek gradyan varyansı $16$. $64$ gradyanın toplamı $64 \cdot 16$; ortalama $\frac{1}{64}$ ile çarpılınca varyans $\frac{64 \cdot 16}{64^2} = \frac{16}{64} = 0{,}25$; standart sapma $0{,}5$.

**Adım 2 — Hedef.** Standart sapma $0{,}25$ ise varyans $0{,}0625 = \frac{16}{n}$, $n = 256$.

**Adım 3 — Dropout.** Açık çıkış $v$ ise $0{,}8 v = 2$, $v = 2{,}5$.

**Neden aynı sonuç?** $\operatorname{Var}(\frac{1}{n}\sum X_i) = \frac{1}{n^2} \cdot n\sigma^2 = \frac{\sigma^2}{n}$: $\frac{\sigma}{\sqrt{n}}$ kuralı buradan geliyor. Dropout sorusu da bir beklenen değer denklemi.

**Cevap:** $0{,}5$; $256$ ve $2{,}5$.
