**Fikir:** Poisson'da beklenen değer $\lambda$; MLE örneklem ortalamasıdır. Bir olasılığın MLE'si, parametrenin MLE'si yerine konarak bulunur.

**Adım 1 — MLE.** $\bar{x} = \frac{24}{6} = 4$.

**Adım 2 — Olasılık.** $P(X = 0) = e^{-\lambda}$ bir $g(\lambda)$; değişmezlikle MLE'si $e^{-\hat{\lambda}} = e^{-4} \approx 0{,}0183$.

**Adım 3 — Eğim.** $\ell'(\lambda) = n\left(\frac{\bar{x}}{\lambda} - 1\right) = 6\left(\frac{4}{5} - 1\right) = -1{,}2$.

**Neden aynı sonuç?** $\frac{\sum x_i}{\lambda} - n = n\left(\frac{\bar{x}}{\lambda} - 1\right)$; türev yalnızca $\bar{x}$'e bağlı olduğu için tahmin de $\bar{x}$ çıkıyor.

**Cevap:** $4$; $0{,}0183$ ve $-1{,}2$.
