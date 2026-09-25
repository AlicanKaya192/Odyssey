**Ne soruluyor?** Doğrusal regresyonun kaybına gradyan inişinin bir adımı ve varılacak nokta.

**Fikir:** $w \leftarrow w - \eta J'(w)$; $J'(w^*) = 0$.

**Adım 1 — Gradyan.** $J'(w) = -2 \cdot 22 + 2w \cdot 14 = -44 + 28w$. $J'(0) = -44$.

**Adım 2 — Bir adım.** $w_1 = 0 - 0{,}01 \cdot (-44) = 0{,}44$.

**Adım 3 — Hedef.** $-44 + 28w = 0$, $w^* = \frac{22}{14} \approx 1{,}571$.

**Sağlama:** $J'(0{,}44) = -44 + 12{,}32 = -31{,}68 < 0$; hâlâ sağa gidilmesi gerekiyor, $w^*$ daha sağda ✓.

**Dikkat:** Gradyanın işareti: negatif gradyan, $w$'yi artırmamız gerektiğini söyler; eksi işaretli güncelleme bunu yapar.

**Cevap:** $-44$; $0{,}44$; $\approx 1{,}571$.
