**Fikir:** EBOB'u Öklid algoritmasıyla bul; fayans sayısını da alanları bölerek hesapla.

**Adım 1 — Öklid.**

$$
\begin{aligned}
840 &= 360 \cdot 2 + 120 \\
360 &= 120 \cdot 3 + 0
\end{aligned}
$$

Kalan $0$: EBOB $120$.

**Adım 2 — Alanlar.** Zeminin alanı $360 \cdot 840$, bir fayansın alanı $120 \cdot 120$. Fayans sayısı alanların oranı:

$$
\frac{360 \cdot 840}{120 \cdot 120} = \frac{360}{120} \cdot \frac{840}{120} = 3 \cdot 7 = 21
$$

Büyük çarpımları hesaplamadan önce her kenarı $120$'ye böldük.

**Neden aynı sonuç?** Alanları bölmek, iki kenardaki fayans sayılarını çarpmakla aynı şey; kesri iki çarpana ayırınca bu açıkça görünüyor. Öklid de çarpanlara ayırmadan aynı EBOB'a varıyor.

**Cevap:** $120$ ve $21$.
