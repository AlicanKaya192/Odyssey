**Fikir:** $D_{\mathrm{KL}}(A \parallel B) = H(A, B) - H(A)$. Her iki yön için ayrı çapraz entropi ve entropi hesapla.

**Adım 1 — $P \parallel Q$.** $H(P, Q) = 1$ (her $q = 0{,}5$), $H(P) \approx 0{,}469$. Fark $0{,}531$.

**Adım 2 — $Q \parallel P$.** $H(Q, P) = -0{,}5\log_2 0{,}9 - 0{,}5\log_2 0{,}1 \approx 0{,}076 + 1{,}661 = 1{,}737$; $H(Q) = 1$. Fark $0{,}737$.

**Adım 3 — $H(P, Q)$.** $1$.

**Neden aynı sonuç?** $\sum a\log\frac{a}{b} = \sum a\log a - \sum a\log b = -H(A) + H(A, B)$. Asimetri buradan da görülüyor: iki yönde hem çapraz entropiler hem de çıkarılan entropiler farklı.

**Cevap:** $0{,}531$; $0{,}737$ ve $1$.
