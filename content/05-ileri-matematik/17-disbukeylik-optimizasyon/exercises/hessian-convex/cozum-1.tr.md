**Ne soruluyor?** İki değişkenli bir fonksiyonun Hessian'ı üzerinden dışbükeyliği.

**Fikir:** Hessian'ın bütün özdeğerleri sıfırdan büyük ya da eşitse fonksiyon dışbükey. İkinci dereceden bir fonksiyonda Hessian sabit, tek bir hesap yeter.

**Adım 1 — Hessian.** $f_{xx} = 4$, $f_{xy} = 2$, $f_{yy} = 2$: $H = \begin{bmatrix} 4 & 2 \\ 2 & 2 \end{bmatrix}$.

**Adım 2 — Determinant.** $4 \cdot 2 - 2 \cdot 2 = 4$.

**Adım 3 — Özdeğerler.** $\lambda^2 - 6\lambda + 4 = 0$: $\lambda = 3 \pm \sqrt{5}$. Küçüğü $3 - \sqrt{5} \approx 0{,}764 > 0$.

**Sağlama:** İki özdeğerin çarpımı $(3 - \sqrt{5})(3 + \sqrt{5}) = 4 = \det H$ ✓, toplamı $6$ = iz ✓. İkisi de pozitif: $f$ kesin dışbükey.

**Dikkat:** $2xy$ teriminin ikinci türevi $f_{xy} = 2$; $f_{xx}$'e katkısı yok.

**Cevap:** $\det H = 4$, küçük özdeğer $\approx 0{,}764$; dışbükey.
