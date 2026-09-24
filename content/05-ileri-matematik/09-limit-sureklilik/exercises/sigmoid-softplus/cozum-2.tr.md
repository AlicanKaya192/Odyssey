**Fikir:** Büyük $x$'te $1 + e^x$ içinde baskın olan $e^x$. Onu çarpan olarak dışarı al: $1 + e^x = e^x(1 + e^{-x})$. Sigmoid için de aynı hareket: pay ve paydayı $e^x$ ile çarp.

**Adım 1 — Sigmoidi yeniden yaz.** $\sigma(x) = \dfrac{e^x}{e^x + 1}$. $x \to -\infty$ iken $e^x \to 0$: $\frac{0}{0 + 1} = 0$. $x \to \infty$ iken payı ve paydayı $e^x$'e böl: $\frac{1}{1 + e^{-x}} \to 1$.

**Adım 2 — Softplus.** $\ln\big(e^x(1 + e^{-x})\big) = x + \ln(1 + e^{-x})$, logaritmanın çarpım kuralıyla.

**Adım 3 — Farkı al.** $s(x) - x = \ln(1 + e^{-x}) \to \ln 1 = 0$.

**Neden aynı sonuç?** $\ln \frac{1 + e^x}{e^x}$ ile $\ln(1 + e^{-x})$ aynı ifade; birincisi bölme kuralıyla, ikincisi çarpım kuralıyla elde ediliyor. İkisi de belirsizliği ortadan kaldıran tek hamle: baskın terimi dışarı almak. Bu sonuç softplus'ın büyük girdilerde neden ReLU gibi davrandığını da gösteriyor: $s(x) \approx x$.

**Cevap:** $1$, $0$, $0$.
