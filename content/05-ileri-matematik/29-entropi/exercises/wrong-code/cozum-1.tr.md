**Ne soruluyor?** Doğru ve yanlış varsayımla ortalama kod uzunluğu ve aradaki fark.

**Fikir:** $H(P) = -\sum p\log_2 p$, $H(P, Q) = -\sum p\log_2 q$, $D_{\mathrm{KL}} = H(P, Q) - H(P)$.

**Adım 1 — $H(P)$.** $\frac{1}{2} \cdot 1 + \frac{1}{4} \cdot 2 + \frac{1}{8} \cdot 3 + \frac{1}{8} \cdot 3 = 1{,}75$.

**Adım 2 — $H(P, Q)$.** Her $q = \frac{1}{4}$: $-\sum p \cdot (-2) = 2$.

**Adım 3 — KL.** $2 - 1{,}75 = 0{,}25$ bit.

**Sağlama:** Doğrudan: $\sum p\log_2\frac{p}{q} = \frac{1}{2} \cdot 1 + \frac{1}{4} \cdot 0 + \frac{1}{8} \cdot (-1) + \frac{1}{8} \cdot (-1) = 0{,}25$ ✓.

**Dikkat:** Çapraz entropide ağırlıklar gerçek dağılım $P$'den gelir, logaritmanın içi varsayılan $Q$'dan; yer değiştirirse başka bir sayı çıkar.

**Cevap:** $1{,}75$; $2$; $0{,}25$.
