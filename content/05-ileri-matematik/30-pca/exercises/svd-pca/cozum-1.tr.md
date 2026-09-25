**Ne soruluyor?** SVD'nin tekil değerlerinden PCA'nın özdeğerlerine ve payına geçmek.

**Fikir:** $X^\mathsf{T}X = VS^2V^\mathsf{T}$; kovaryans $\frac{1}{n - 1}X^\mathsf{T}X$, özdeğerleri $\frac{s_j^2}{n - 1}$.

**Adım 1 — $\lambda_1$.** $\frac{400}{10} = 40$.

**Adım 2 — $\lambda_3$.** $\frac{25}{10} = 2{,}5$. ($\lambda_2 = 10$.)

**Adım 3 — Pay.** $\frac{40}{40 + 10 + 2{,}5} = \frac{40}{52{,}5} \approx 0{,}762$.

**Sağlama:** Tekil değerler yarıya inerken özdeğerler dörtte birine iniyor ($40 \to 10 \to 2{,}5$): kare ilişkisi ✓.

**Dikkat:** Payı tekil değerlerle doğrudan hesaplamak ($\frac{20}{35} \approx 0{,}571$) yanlış; varyans tekil değerin karesiyle orantılı.

**Cevap:** $40$; $2{,}5$; $\approx 0{,}762$.
