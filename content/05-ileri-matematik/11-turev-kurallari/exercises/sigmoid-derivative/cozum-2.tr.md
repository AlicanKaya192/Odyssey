**Fikir:** $\sigma(1 - \sigma)$ biçimine güvenmeden, zincir kuralından çıkan $\sigma'(x) = \dfrac{e^{-x}}{(1 + e^{-x})^2}$ formülüne doğrudan koy.

**Adım 1 — $x = 0$.** $e^0 = 1$: $\frac{1}{(1 + 1)^2} = \frac{1}{4}$.

**Adım 2 — $x = \ln 3$.** $e^{-x} = \frac{1}{3}$:

$$
\frac{1/3}{(4/3)^2} = \frac{1}{3} \cdot \frac{9}{16} = \frac{3}{16}
$$

**Adım 3 — Dört katman.** $\frac{1}{4^4} = \frac{1}{256}$.

**Neden aynı sonuç?** $\frac{e^{-x}}{(1 + e^{-x})^2}$ ile $\sigma(1 - \sigma)$ aynı ifadenin iki yazılışı; dersteki cebir bunu gösterdi. Pratikte ikinci yazım kazanıyor: $\sigma$ ileri geçişte hesaplanmış olduğu için türev tek bir çarpma.

**Cevap:** $\frac{1}{4}$, $\frac{3}{16}$, $\frac{1}{256}$.
