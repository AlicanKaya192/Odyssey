**Fikir:** $J'(w) = 28(w - w^*)$ olduğundan güncelleme $w_{t+1} - w^* = (1 - 28\eta)(w_t - w^*)$ olur: hata her adımda sabit bir oranla küçülür.

**Adım 1 — $w^*$ ve gradyan.** $w^* = \frac{22}{14} \approx 1{,}571$; $J'(0) = 28(0 - 1{,}571) = -44$.

**Adım 2 — Bir adım.** Oran $1 - 0{,}28 = 0{,}72$. $w_1 - w^* = 0{,}72 \cdot (-1{,}571)$, yani $w_1 = 0{,}28 \cdot 1{,}571 = 0{,}44$.

**Adım 3 — Sonuç.** Hata her adımda $0{,}72$ ile çarpılıyor; $w_t \to w^* \approx 1{,}571$.

**Neden aynı sonuç?** İkinci dereceden bir kayıpta gradyan, en küçük noktaya uzaklıkla orantılı; bu yüzden gradyan inişi geometrik bir hızla aynı çözüme, normal denklemlerin çözümüne gider. $\eta > \frac{2}{28}$ olsaydı oranın mutlak değeri $1$'i aşar ve adımlar ıraksardı.

**Cevap:** $-44$; $0{,}44$ ve $1{,}571$.
