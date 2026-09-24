**Ne soruluyor?** Tabloda kaç bağımsız bilgi olduğu (rank) ve modelin ağırlıklarını belirsiz bırakan yön (çekirdek).

**Fikir:** Rank = bağımsız sütun sayısı. Sütunlar arasındaki ilişkiyi bulursak hem rankı hem çekirdeği okuruz.

**Adım 1 — 3. sütun.** $1.2 = 120 / 100$, $0.8 = 80 / 100$, … her satırda 3. sütun 1. sütunun $\tfrac{1}{100}$'ü:

$$
\mathbf{a}_3 = \tfrac{1}{100}\,\mathbf{a}_1
$$

3. sütun fazlalık; yeni bir yön eklemiyor.

**Adım 2 — 1. ve 2. sütun bağımsız mı?** $120 / 3 = 40$, $80 / 2 = 40$ ama $150 / 4 = 37.5$. Oran sabit değil: $\mathbf{a}_1$, $\mathbf{a}_2$'nin katı değil. İkisi bağımsız.

**Adım 3 — Rank.** İki bağımsız sütun, üçüncü onlardan birinin katı: $\operatorname{rank} X = 2$.

**Adım 4 — Çekirdek.** $X(1, 0, c) = \mathbf{a}_1 + c\,\mathbf{a}_3 = \mathbf{a}_1 + \tfrac{c}{100}\,\mathbf{a}_1 = \left(1 + \tfrac{c}{100}\right)\mathbf{a}_1$. Bunun sıfır olması için:

$$
\begin{aligned}
1 + \frac{c}{100} &= 0 \\
c &= -100
\end{aligned}
$$

**Sağlama:** 1. satırda $120 \cdot 1 + 3 \cdot 0 + 1.2 \cdot (-100) = 120 - 120 = 0$ ✓; öteki satırlar da aynı şekilde sıfır.

**Sonucu yorumla:** Bir modelin ağırlıkları $\mathbf{w}$ ise $\mathbf{w} + t\,(1, 0, -100)$ de **tamamen aynı** tahminleri verir: 1. özelliğe 1 birim fazla ağırlık, 3. özelliğe 100 birim az ağırlık birbirini götürüyor. Veri bu ağırlıkları birbirinden ayıramıyor; çözüm fazlalık olan sütunu atmak.

**Cevap:** $\operatorname{rank} X = 2$, $c = -100$.
