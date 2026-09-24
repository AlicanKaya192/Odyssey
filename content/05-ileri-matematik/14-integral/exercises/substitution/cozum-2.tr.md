**Fikir:** Birinci integrali açıp polinom olarak; ikinciyi ters türevi tahmin edip türevle doğrulayarak çöz.

**Adım 1 — Aç.** $(x^2 + 1)^3 = x^6 + 3x^4 + 3x^2 + 1$; $2x$ ile çarp: $2x^7 + 6x^5 + 6x^3 + 2x$.

**Adım 2 — İntegral.**

$$
\left[\frac{x^8}{4} + x^6 + \frac{3x^4}{2} + x^2\right]_0^1 = \frac{1}{4} + 1 + \frac{3}{2} + 1 = \frac{15}{4}
$$

**Adım 3 — Tahmin.** $(e^{2x})' = 2e^{2x}$; yarısı yeter: $F = \frac{e^{2x}}{2}$. $F(\ln 2) - F(0) = \frac{4}{2} - \frac{1}{2} = \frac{3}{2}$.

**Neden aynı sonuç?** $\frac{(x^2 + 1)^4}{4}$'ü açarsan $\frac{x^8}{4} + x^6 + \frac{3x^4}{2} + x^2 + \frac{1}{4}$ çıkar: aynı ters türev, yalnızca sabit farkı ($\frac{1}{4}$) var ve belirli integralde sadeleşiyor. Değişken değiştirme uzun açılımı atlamanın kısa yolu.

**Cevap:** $\frac{15}{4}$ ve $\frac{3}{2}$.
