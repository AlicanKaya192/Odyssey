**Ne soruluyor?** Lojistik regresyonda tek bir gradyan inişi adımı.

**Fikir:** $\frac{\partial\,\text{kayıp}}{\partial w} = (p - y)x$.

**Adım 1 — $p$.** $z = 0{,}5 \cdot 2 - 0{,}5 = 0{,}5$. $p = \frac{1}{1{,}6065} \approx 0{,}622$.

**Adım 2 — Türev.** $(0{,}622 - 1) \cdot 2 \approx -0{,}755$.

**Adım 3 — Güncelleme.** $w = 0{,}5 - 0{,}1 \cdot (-0{,}755) \approx 0{,}5755$.

**Sağlama:** Yeni $z = 0{,}5755 \cdot 2 + b$; $w$ arttığı için $z$ ve $p$ artar, kayıp ($-\ln p$) azalır ✓.

**Dikkat:** Gradyanın işareti negatif; güncelleme onu çıkardığı için $w$ büyür. Türevi $(y - p)x$ yazıp aynı güncellemeyi yapmak $w$'yi yanlış yöne götürür.

**Cevap:** $\approx 0{,}622$; $\approx -0{,}755$; $\approx 0{,}5755$.
