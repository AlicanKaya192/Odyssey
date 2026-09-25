**Fikir:** Oran biçiminde her özellik kendi olabilirlik oranıyla çarpar.

**Adım 1 — Oranlar.** Önsel $\frac{0{,}4}{0{,}6} = \frac{2}{3}$. Birinci kelime var: $\frac{0{,}5}{0{,}1} = 5$; yok: $\frac{0{,}5}{0{,}9} = \frac{5}{9}$. İkinci kelime var: $\frac{0{,}2}{0{,}25} = 0{,}8$. İki kelimeli e-postanın spam puanı Bayes payından: $0{,}04$.

**Adım 2 — İki kelime.** $\frac{2}{3} \cdot 5 \cdot 0{,}8 = \frac{8}{3}$. Olasılık $\frac{8/3}{1 + 8/3} = \frac{8}{11}$.

**Adım 3 — Yalnız ikinci.** $\frac{2}{3} \cdot \frac{5}{9} \cdot 0{,}8 = \frac{8}{27}$. Olasılık $\frac{8/27}{1 + 8/27} = \frac{8}{35}$.

**Neden aynı sonuç?** Puanların oranı $\frac{0{,}04}{0{,}015} = \frac{8}{3}$, olabilirlik oranlarının çarpımına eşit; Naive Bayes, oran biçiminde her kelimenin "ne kadar spam kokduğunu" çarparak birleştiriyor.

**Cevap:** $0{,}04$; $\frac{8}{11}$ ve $\frac{8}{35}$.
