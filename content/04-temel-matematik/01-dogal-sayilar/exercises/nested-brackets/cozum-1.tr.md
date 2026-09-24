**Ne soruluyor?** İç içe parantezli bir ifadenin değeri.

**Fikir:** İç içe parantezlerde en içtekinden başlanır. Her parantezin **içinde de** işlem önceliği geçerli: önce üs, sonra çarpma, en son toplama ve çıkarma.

**Adım 1 — En içteki parantez: $(15 - 3 \cdot 4)$.** İçinde çarpma çıkarmadan önce:

$$
15 - 3 \cdot 4 = 15 - 12 = 3
$$

İfade şimdi:

$$
100 - [4 \cdot 3 + 2^3]
$$

**Adım 2 — Köşeli parantezin içi.** Önce üs, sonra çarpma, en son toplama:

$$
\begin{aligned}
4 \cdot 3 + 2^3 &= 4 \cdot 3 + 8 \\
&= 12 + 8 = 20
\end{aligned}
$$

**Adım 3 — Dıştaki işlem.**

$$
100 - 20 = 80
$$

**Dikkat:** En içteki parantezi soldan sağa yapıp $(15 - 3) \cdot 4 = 48$ bulmak en sık hata; parantezin içinde de çarpma önce. Bir başka tuzak $2^3$'ü $2 \cdot 3 = 6$ sanmak.

**Cevap:** $80$.
