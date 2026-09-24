**Fikir:** Hacmi polinom olarak açıp kuvvet kuralıyla türevle, sonra ikinci türevle doğrula.

**Adım 1 — Aç.** $(12 - 2x)^2 = 144 - 48x + 4x^2$; $V(x) = 4x^3 - 48x^2 + 144x$.

**Adım 2 — Türev.** $V'(x) = 12x^2 - 96x + 144 = 12(x^2 - 8x + 12) = 12(x - 2)(x - 6)$.

**Adım 3 — Doğrula.** $V''(x) = 24x - 96$; $V''(2) = -48 < 0$: en büyük. $V(2) = 32 - 192 + 288 = 128$.

**Neden aynı sonuç?** $12(x - 2)(x - 6)$ ile $(12 - 2x)(12 - 6x)$ aynı polinom: $(12 - 2x)(12 - 6x) = 2(6 - x) \cdot 6(2 - x) = 12(x - 6)(x - 2)$. Açmak daha uzun ama zincir kuralında işaret hatası riski yok.

**Cevap:** $2$ ve $128$.
