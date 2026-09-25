**Ne soruluyor?** Bir hiperparametre aramasının ve bir özellik seçiminin büyüklüğü.

**Fikir:** Bağımsız ayarlar çarpılır. Özellik alt kümeleri sırasız seçim; bütün alt kümeler $2^n$.

**Adım 1 — Izgara.** $5 \cdot 4 \cdot 3 = 60$ ayar, her biri $5$ eğitim: $300$.

**Adım 2 — Tam $3$ özellik.** $\binom{10}{3} = \frac{10 \cdot 9 \cdot 8}{6} = 120$.

**Adım 3 — Boş olmayan.** $2^{10} - 1 = 1023$.

**Sağlama:** Tam $3$ özellikli alt kümeler bütün alt kümelerin küçük bir kısmı olmalı: $120 < 1023$ ✓.

**Dikkat:** Özellik alt kümesinde sıra önemsiz: $\{x_1, x_2, x_3\}$ ile $\{x_3, x_1, x_2\}$ aynı model. $P(10, 3) = 720$ her alt kümeyi $6$ kez sayar.

**Cevap:** $300$, $120$, $1023$.
