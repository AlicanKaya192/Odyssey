**Ne soruluyor?** Bağımsız denemelerde belli sayıda başarı, beklenen başarı ve en az bir başarı.

**Fikir:** $8$ bağımsız evet–hayır denemesi: $X \sim$ Binom$(8; 0{,}25)$.

**Adım 1 — Tam $2$.** $\binom{8}{2} = 28$; $0{,}25^2 = 0{,}0625$; $0{,}75^6 \approx 0{,}17798$.

$$
P(X = 2) = 28 \cdot 0{,}0625 \cdot 0{,}17798 \approx 0{,}3115
$$

**Adım 2 — Beklenen değer.** $np = 8 \cdot 0{,}25 = 2$.

**Adım 3 — En az bir.** $P(X = 0) = 0{,}75^8 \approx 0{,}1001$; $1 - 0{,}1001 = 0{,}8999$.

**Sağlama:** En olası değer beklenen değerin yakınında olmalı: $P(X = 1) = 8 \cdot 0{,}25 \cdot 0{,}75^7 \approx 0{,}267$, $P(X = 2) \approx 0{,}311$, $P(X = 3) \approx 0{,}208$; tepe $2$'de ✓.

**Dikkat:** $\binom{8}{2}$'yi unutmak yalnızca "ilk ikisi tıkladı, gerisi tıklamadı" sırasını sayar ($0{,}0111$).

**Cevap:** $\approx 0{,}3115$; $2$; $\approx 0{,}8999$.
