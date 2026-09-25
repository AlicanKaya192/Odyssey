**Fikir:** Sonsuz ödül toplamı $V$ ise, ilk adımdan sonrası yine aynı toplamın $\gamma$ katı: $V = 2 + \gamma V$. Pekiştirmeli öğrenmedeki Bellman denkleminin en basit hâli.

**Adım 1 — MSE.** Birinci çözümdeki gibi: $\frac{1 + 0 + 4 + 1}{4} = 1{,}5$.

**Adım 2 — $V$.** $V = 2 + 0{,}8 V$, yani $0{,}2 V = 2$ ve $V = 10$.

**Adım 3 — Ağırlıklar.** Bütün ağırlıkların toplamı $W = (1 - \beta) + \beta W$, buradan $W = 1$. İlk üçünden sonrası $\beta^3 W = 0{,}125$; ilk üçü $1 - 0{,}125 = 0{,}875$.

**Neden aynı sonuç?** "$S = a_1 + rS$" eşitliği, geometrik serinin $S - rS = a_1$ hilesinin başka bir yazılışı. Sonsuz bir toplamın kendi içinde kendisinin küçültülmüş bir kopyası var; bu, formülü ezberlemeden kullanmanın yolu.

**Cevap:** $1{,}5$, $10$ ve $0{,}875$.
