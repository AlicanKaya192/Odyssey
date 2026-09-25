**Fikir:** $\ell = -\frac{n}{2}\ln(2\pi v) - \frac{1}{2v}\sum(x_i - \mu)^2$, $v = \sigma^2$. İki kısmi türevi sıfıra eşitle.

**Adım 1 — $\mu$.** $\frac{\partial\ell}{\partial\mu} = \frac{1}{v}\sum(x_i - \mu) = 0$; $\sum x_i = 5\mu$, $\hat{\mu} = 12$.

**Adım 2 — $v$.**

$$
\frac{\partial\ell}{\partial v} = -\frac{n}{2v} + \frac{S}{2v^2} = 0
$$

Burada $S = \sum(x_i - \hat{\mu})^2 = 26$; çözüm $v = \frac{S}{n} = 5{,}2$.

**Adım 3 — Yansız.** $\frac{S}{n - 1} = 6{,}5$; MLE bu düzeltmeyi yapmaz.

**Neden aynı sonuç?** Hazır formüller tam bu iki denklemin çözümü; $v$ denkleminde $n$ doğrudan olabilirlikten geliyor, $n - 1$ ise ayrı bir yansızlık isteğinden.

**Cevap:** $12$; $5{,}2$ ve $6{,}5$.
