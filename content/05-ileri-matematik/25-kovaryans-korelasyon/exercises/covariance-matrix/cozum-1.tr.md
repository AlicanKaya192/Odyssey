**Ne soruluyor?** Merkezlenmiş veri matrisinden kovaryans matrisi ve korelasyon.

**Fikir:** $X^\mathsf{T}X$'in elemanları sütunların iç çarpımları; $n - 1$'e bölününce kovaryanslar çıkar.

**Adım 1 — $\Sigma_{11}$.** Birinci sütunun kendisiyle iç çarpımı $4 + 1 + 0 + 1 + 4 = 10$; $\frac{10}{4} = 2{,}5$.

**Adım 2 — $\Sigma_{12}$.** Sütunların iç çarpımı $2 + 2 + 0 + 1 + 4 = 9$; $\frac{9}{4} = 2{,}25$. İkinci sütun da $\frac{10}{4} = 2{,}5$:

$$
\Sigma = \begin{pmatrix} 2{,}5 & 2{,}25 \\ 2{,}25 & 2{,}5 \end{pmatrix}
$$

**Adım 3 — Korelasyon.** $r = \frac{2{,}25}{\sqrt{2{,}5 \cdot 2{,}5}} = 0{,}9$.

**Sağlama:** $\Sigma$ simetrik; $w = (1, -1)$ için $w^\mathsf{T}\Sigma w = 2{,}5 + 2{,}5 - 4{,}5 = 0{,}5 \geq 0$ ✓ (pozitif yarı tanımlı).

**Dikkat:** $XX^\mathsf{T}$ hesaplamak $5 \times 5$ bir matris verir; kovaryans matrisi özellik sayısı kadar, $2 \times 2$ olmalı.

**Cevap:** $2{,}5$; $2{,}25$; $0{,}9$.
