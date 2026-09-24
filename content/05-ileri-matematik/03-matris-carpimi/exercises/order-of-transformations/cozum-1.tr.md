**Ne soruluyor?** Aynı iki dönüşüm, iki farklı sırada. Sonuçların farklı çıkıp çıkmadığını göreceğiz.

**Fikir:** Her matrisin ne yaptığını kurala çevir, sonra vektöre sırayla uygula:

- $R$: $(x, y) \to (-y,\ x)$ (çeyrek tur sola)
- $S$: $(x, y) \to (x,\ -y)$ ($x$ ekseninde ayna)

**1. sıra — Adım 1: döndür.** $(1, 3) \to (-3,\ 1)$.

**1. sıra — Adım 2: yansıt.** $y$'nin işareti değişiyor: $(-3, 1) \to (-3,\ -1)$.

**2. sıra — Adım 1: yansıt.** $(1, 3) \to (1,\ -3)$.

**2. sıra — Adım 2: döndür.** $(x, y) = (1, -3)$ için $(-y, x) = (3,\ 1)$.

**Sonucu yorumla:** İki sonuç birbirinin tam tersi: $(-3, -1)$ ile $(3, 1)$. Aynı iki hareket, yalnızca sıraları değişince vektörü zıt yönlere gönderdi. Matris çarpımının değişmeli olmamasının geometrideki görüntüsü bu.

**Sağlama:** Döndürme ve yansıma uzunluğu korur. $\|(1, 3)\| = \sqrt{10}$ ve iki sonucun uzunluğu da $\sqrt{9 + 1} = \sqrt{10}$. ✓

**Cevap:** 1. sıra $(-3, -1)$; 2. sıra $(3, 1)$.
