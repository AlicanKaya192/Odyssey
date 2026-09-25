**Fikir:** Standart hata $\sqrt{n}$ ile ters orantılı; bir değer bilinince ötekiler oranla bulunur.

**Adım 1 — Başlangıç.** $n = 36$'da $4$.

**Adım 2 — Yarıya.** Hatayı $2$ kat küçültmek için $n$ $2^2 = 4$ kat: $144$.

**Adım 3 — Dörtte bire.** $576 = 16 \cdot 36$; $\sqrt{16} = 4$, hata $\frac{4}{4} = 1$.

**Neden aynı sonuç?** $\frac{\text{SE}_1}{\text{SE}_2} = \sqrt{\frac{n_2}{n_1}}$; formülün oran hâli, $\sigma$'yı bilmeden de çalışıyor.

**Cevap:** $4$; $144$ ve $1$.
