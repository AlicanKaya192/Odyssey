**Fikir:** $e^x$'i özel yapan $f' = f$ ve $f(0) = 1$. Katsayıları bu iki koşuldan, türev tablosu kullanmadan bulalım: $P(x) = c_0 + c_1 x + c_2 x^2 + c_3 x^3 + \cdots$ için $P' = P$ iste.

**Adım 1 — Karşılaştır.** $P' = c_1 + 2c_2 x + 3c_3 x^2 + \cdots$. Aynı kuvvetlerin katsayıları eşit: $c_1 = c_0$, $2c_2 = c_1$, $3c_3 = c_2$.

**Adım 2 — Zincirleme.** $c_0 = 1$ ($P(0) = 1$), $c_1 = 1$, $c_2 = \frac{1}{2}$, $c_3 = \frac{1}{6}$.

**Adım 3 — Değer.** $1 + 0{,}5 + 0{,}125 + 0{,}0208\overline{3} = 1{,}6458\overline{3} = \frac{79}{48}$.

**Neden aynı sonuç?** $c_{k+1} = \frac{c_k}{k + 1}$ kuralı adım adım $c_k = \frac{1}{k!}$ üretiyor; faktöriyel, "türevi kendisine eşit" koşulunun doğal sonucu. Taylor formülü aynı şeyi türevlerden söylüyor.

**Cevap:** $\frac{1}{6}$ ve $\frac{79}{48} \approx 1{,}6458$.
