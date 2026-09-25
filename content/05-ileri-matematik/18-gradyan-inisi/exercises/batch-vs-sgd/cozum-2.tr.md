**Fikir:** Tam gradyanı örnekleri ayırmadan, ortalama kaybı $w$'nin polinomu olarak yazıp bul; SGD için örnek kayıplarını ayrı ayrı yaz.

**Adım 1 — Ortalama kayıp.** $L = \frac{1}{2}\big((2 - w)^2 + (3 - 3w)^2\big) = \frac{1}{2}(10w^2 - 22w + 13)$. $L'(w) = 10w - 11$; $L'(0) = -11$.

**Adım 2 — Tam adım.** $0 + 0{,}05 \cdot 11 = 0{,}55$.

**Adım 3 — SGD.** $\ell_2 = 9(1 - w)^2$, $\ell_2' = -18(1 - w)$; $w = 0$'da $-18$, $w = 0{,}9$. $\ell_1 = (2 - w)^2$, $\ell_1'(0{,}9) = -2{,}2$; $w = 1{,}01$.

**Neden aynı sonuç?** Ortalamanın türevi türevlerin ortalaması: $10w - 11 = \frac{1}{2}\big(-2(2 - w) - 18(1 - w)\big)$. Açık formül ayrıca en iyi noktayı da veriyor: $L' = 0 \Rightarrow w = 1{,}1$.

**Cevap:** $-11$, $0{,}55$, $1{,}01$.
