**Ne soruluyor?** İki yöndeki KL ıraksaması ve çapraz entropi.

**Fikir:** $D_{\mathrm{KL}}(A \parallel B) = \sum a\log_2\frac{a}{b}$; ağırlıklar ilk dağılımdan.

**Adım 1 — $P \parallel Q$.** $0{,}9 \cdot 0{,}848 + 0{,}1 \cdot (-2{,}322) \approx 0{,}763 - 0{,}232 = 0{,}531$.

**Adım 2 — $Q \parallel P$.** $0{,}5 \cdot (-0{,}848) + 0{,}5 \cdot 2{,}322 \approx -0{,}424 + 1{,}161 = 0{,}737$.

**Adım 3 — $H(P, Q)$.** $-0{,}9\log_2 0{,}5 - 0{,}1\log_2 0{,}5 = 1$.

**Sağlama:** $H(P) \approx 0{,}469$ ve $H(P, Q) - H(P) = 1 - 0{,}469 = 0{,}531$ ✓.

**Dikkat:** İki KL farklı: $Q \parallel P$ daha büyük, çünkü $Q$'nun yarı yarıya verdiği ikinci sonuca $P$ yalnızca $0{,}1$ olasılık veriyor; o terim ağır basıyor.

**Cevap:** $\approx 0{,}531$; $\approx 0{,}737$; $1$.
