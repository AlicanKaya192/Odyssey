**Fikir:** En iyi kodda A, B, C, D için uzunluklar $1, 2, 3, 3$ bit (kodlar $0$, $10$, $110$, $111$). Mühendisin kodunda hepsi $2$ bit.

**Adım 1 — En iyi kod.** Ortalama uzunluk $\frac{1}{2} \cdot 1 + \frac{1}{4} \cdot 2 + \frac{1}{4} \cdot 3 = 1{,}75$.

**Adım 2 — Mühendisin kodu.** Her durum $2$ bit; ortalama $2$.

**Adım 3 — Kayıp.** Sonuç başına $0{,}25$ bit fazladan; bir milyon ölçümde $250\,000$ bit.

**Neden aynı sonuç?** Olasılıklar $2$'nin kuvvetleri olduğu için en iyi kodun uzunlukları tam olarak $-\log_2 p$; varsayılan $Q$'nun kodunun uzunlukları $-\log_2 q$. Ortalama uzunluklar da tam olarak $H(P)$ ve $H(P, Q)$.

**Cevap:** $1{,}75$; $2$ ve $0{,}25$.
