**Fikir:** Tekrarlı harfler için bölmek yerine, $7$ yerden her harfin gideceği yerleri kombinasyonla seç.

**Adım 1 — KALEM.** K için $5$ yer, A için kalan $4$, … $5 \cdot 4 \cdot 3 \cdot 2 \cdot 1 = 120$.

**Adım 2 — BALABAN.** Üç A'nın yeri: $\binom{7}{3} = 35$. Kalan $4$ yerden iki B'nin yeri: $\binom{4}{2} = 6$. Kalan $2$ yere L ve N: $2$ yol. Toplam $35 \cdot 6 \cdot 2 = 420$.

**Adım 3 — K ile başlayan.** İlk yer K'ya ayrıldı; A, L, E, M kalan $4$ yere: $4 \cdot 3 \cdot 2 \cdot 1 = 24$.

**Neden aynı sonuç?** $\binom{7}{3}\binom{4}{2} \cdot 2! = \frac{7!}{3!4!} \cdot \frac{4!}{2!2!} \cdot 2! = \frac{7!}{3!2!}$: yer seçmek ve fazla sayılanı bölmek aynı hesabın iki yazılışı.

**Cevap:** $120$, $420$ ve $24$.
