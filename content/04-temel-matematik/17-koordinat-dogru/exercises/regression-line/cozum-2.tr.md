**Fikir:** Eğim, $x$ bir artınca tahminin ne kadar değiştiği. Bunu bulunca tahmin tablosunu birim birim yürüyerek dolduralım.

**Adım 1 — Birim başına değişim.** $x$, $2$'den $6$'ya $4$ birim artınca tahmin $7$'den $19$'a $12$ artıyor. Birim başına $12 / 4 = 3$: $w = 3$.

**Adım 2 — Geriye yürümek.** $x = 2$'den $x = 0$'a iki birim geri: $7 - 2 \cdot 3 = 1$. $x = 0$'daki tahmin $b$'nin kendisi: $b = 1$.

**Adım 3 — İleri yürümek.** $x = 2$'den $x = 4$'e iki birim ileri: $7 + 2 \cdot 3 = 13$. Gerçek değer $15$, hata $2$.

**Neden aynı sonuç?** Doğrusal modelde her birim adım tahmine aynı $w$'yi ekler; eğim formülü de toplam değişimi adım sayısına bölerek bu sabit adımı buluyor. $b$ ise tanım gereği $x = 0$'daki değer.

**Cevap:** $3$, $1$ ve $2$.
