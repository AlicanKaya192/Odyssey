**Fikir:** $\Sigma$'nın sütunları $(4, 2)$ ve $(2, 1)$ birbirinin katı; matris tek bir yönü "görüyor": $(2, 1)$.

**Adım 1 — Yön varyansı.** $\Sigma(1, 1) = (6, 3)$; $\frac{1}{2}(1, 1) \cdot (6, 3) = 4{,}5$.

**Adım 2 — $\lambda_1$.** $\Sigma(2, 1) = (10, 5) = 5 \cdot (2, 1)$: $\lambda_1 = 5$.

**Adım 3 — $\lambda_2$.** Dik yön $(1, -2)$: $\Sigma(1, -2) = (0, 0)$, $\lambda_2 = 0$.

**Neden aynı sonuç?** Determinantın sıfır olması, bir yönün matris tarafından sıfıra gönderilmesi demek; o yön $\lambda = 0$'ın özvektörü. İz de kalan tek özdeğeri verir. Bu veride PCA ile $1$ boyuta inmek hiç bilgi kaybettirmez.

**Cevap:** $4{,}5$; $5$ ve $0$.
