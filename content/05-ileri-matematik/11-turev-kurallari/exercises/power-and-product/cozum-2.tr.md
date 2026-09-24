**Fikir:** Çarpım kuralı yerine çarpımı açıp polinom olarak türevlemek; $f$ için de her terimi ayrı ayrı, tablodaki türevlerle hesaplamak.

**Adım 1 — $f'(4)$, terim terim.** $(x^3)' = 3x^2 \to 48$. $(\sqrt{x})' = \frac{1}{2\sqrt{x}} \to \frac{1}{4}$, çarpı $-4$: $-1$. $(\frac{1}{x})' = -\frac{1}{x^2} \to -\frac{1}{16}$, çarpı $2$: $-\frac{1}{8}$. Toplam $48 - 1 - \frac{1}{8} = \frac{375}{8}$.

**Adım 2 — $h$'yi aç.** $(x^2 + 1)(x - 3) = x^3 - 3x^2 + x - 3$.

**Adım 3 — Türev.** $h'(x) = 3x^2 - 6x + 1$; $h'(2) = 12 - 12 + 1 = 1$.

**Neden aynı sonuç?** Çarpım kuralının sonucu $2x(x - 3) + x^2 + 1 = 2x^2 - 6x + x^2 + 1 = 3x^2 - 6x + 1$; açıp türevlemekle birebir aynı polinom. Çarpım kuralı, açması zor çarpımlarda (örneğin $x^2 e^x$) gerçekten gerekli; burada iki yol da kısa.

**Cevap:** $\frac{375}{8}$ ve $1$.
