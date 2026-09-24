**Ne soruluyor?** İki aktivasyonun sonsuzdaki davranışı.

**Fikir:** Hepsinde anahtar $e^{-x}$: $x \to \infty$ iken sıfıra gider, $x \to -\infty$ iken sınırsız büyür. Üçüncüde $\infty - \infty$ belirsizliği var; logaritmaları birleştirip bir terime indirmek gerekiyor.

**Adım 1 — Sigmoid, artı sonsuz.** $e^{-x} \to 0$: $\sigma(x) \to \frac{1}{1 + 0} = 1$.

**Adım 2 — Sigmoid, eksi sonsuz.** $e^{-x} \to \infty$: payda sınırsız büyür, $\sigma(x) \to 0$.

**Adım 3 — Softplus eksi $x$.**

$$
\begin{aligned}
\ln(1 + e^x) - x &= \ln(1 + e^x) - \ln e^x \\
&= \ln \frac{1 + e^x}{e^x} = \ln\left(e^{-x} + 1\right)
\end{aligned}
$$

$x \to \infty$ iken $e^{-x} + 1 \to 1$ ve $\ln 1 = 0$.

**Sağlama:** $x = 10$: $e^{-10} \approx 0{,}000045$; $\ln(1{,}000045) \approx 0{,}000045$. Sıfıra çok yakın ✓.

**Dikkat:** $\ln(1 + e^x) - x$'i doğrudan "$\infty - \infty = 0$" diye bitirmek doğru sonuca yanlış yoldan varmak olur; aynı akıl yürütme $\ln(1 + e^x) - x/2$ için de $0$ derdi, oysa o sınırsız büyür. Belirsiz biçim dönüştürülmeden karar verilmez.

**Cevap:** $1$, $0$ ve $0$.
