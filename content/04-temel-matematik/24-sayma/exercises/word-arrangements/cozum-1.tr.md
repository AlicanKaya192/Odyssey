**Ne soruluyor?** Farklı harfli ve tekrarlı harfli kelimelerin dizilim sayıları, bir de ilk harfi sabit dizilimler.

**Fikir:** $n$ farklı nesne $n!$ sırada dizilir. Aynı nesneler varsa kendi aralarındaki yer değiştirmeler yeni diziliş vermez; onlara bölünür.

**Adım 1 — KALEM.** $5$ farklı harf: $5! = 120$.

**Adım 2 — BALABAN.** $7$ harf; A $3$, B $2$, L ve N birer kez:

$$
\frac{7!}{3! \cdot 2!} = \frac{5040}{12} = 420
$$

**Adım 3 — K ile başlayanlar.** İlk yer K; kalan $4$ farklı harf $4! = 24$ sırada.

**Sağlama:** $5$ harfin her biri ilk yerde eşit sıklıkta: $\frac{120}{5} = 24$ ✓.

**Dikkat:** BALABAN'da $7!$ yazıp bırakmak aynı dizilimi $12$ kez saymak olur (A'ların $3!$, B'lerin $2!$ yer değiştirmesi).

**Cevap:** $120$, $420$, $24$.
