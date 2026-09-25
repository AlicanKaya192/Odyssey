**Fikir:** $X = X_1 + \dots + X_8$; her $X_i$ bir Bernoulli($0{,}25$). Beklenen değer doğrusallıkla, olasılıklar sayma ve bağımsızlıkla.

**Adım 1 — Tam $2$.** Tıklayan iki kişi $\binom{8}{2} = 28$ şekilde seçilir; her seçimin olasılığı $0{,}25^2 \cdot 0{,}75^6$ (bağımsızlık). Çarpım $\approx 0{,}3115$.

**Adım 2 — Beklenen değer.** $E[X] = \sum E[X_i] = 8 \cdot 0{,}25 = 2$; dağılımı bilmeden.

**Adım 3 — En az bir.** Hiç kimsenin tıklamaması, $8$ bağımsız "hayır": $0{,}75^8$. Tümleyen $0{,}8999$.

**Neden aynı sonuç?** Binom formülü bu üç adımın kısaltması: $\binom{n}{k}$ seçim, $p^k(1 - p)^{n - k}$ bağımsızlık, $np$ doğrusallık.

**Cevap:** $0{,}3115$; $2$ ve $0{,}8999$.
