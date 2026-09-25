**Ne soruluyor?** İki kritik noktanın türü ve en küçük değer.

**Fikir:** Hessian'ın her kritik noktadaki özdeğerlerine (ya da determinant ve köşegenine) bak.

**Adım 1 — Hessian.** $H = \begin{bmatrix} 6x & 0 \\ 0 & 2 \end{bmatrix}$: köşegen, özdeğerleri $6x$ ve $2$.

**Adım 2 — $(1, 0)$.** Özdeğerler $6$ ve $2$, ikisi de pozitif: en küçük. $f(1, 0) = 1 - 3 = -2$.

**Adım 3 — $(-1, 0)$.** Özdeğerler $-6$ ve $2$: işaretler farklı, eyer. $\det H = -12$.

**Sağlama:** $(-1, 0)$'dan $x$ yönünde çıkınca $f$ azalıyor ($f(-1{,}1; 0) = 1{,}969 < 2$), $y$ yönünde artıyor ($f(-1; 0{,}1) = 2{,}01 > 2$): eyer ✓.

**Dikkat:** $(-1, 0)$'daki değer $f = 2$, yerel en büyük gibi görünebilir; ama $y$ yönünde dip. Tek bir yöne bakmak yanıltır.

**Cevap:** $x = 1$, değer $-2$, $\det H = -12$.
