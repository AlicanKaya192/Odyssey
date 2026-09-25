**Ne soruluyor?** Bağımsız denemelerde "en az bir" ve "tam bir"; sonlu bir gruptan iadesiz seçimde "en az bir".

**Fikir:** "En az bir" için tümleyen; bağımsızlıkta olasılıklar çarpılır; iadesiz seçimde kombinasyonla say.

**Adım 1 — En az bir.** Hiç premium yok: $0{,}7^3 = 0{,}343$. $1 - 0{,}343 = 0{,}657$.

**Adım 2 — Tam bir.** Bir sıralama için $0{,}3 \cdot 0{,}7 \cdot 0{,}7 = 0{,}147$; premium olan $3$ kullanıcıdan herhangi biri olabilir: $3 \cdot 0{,}147 = 0{,}441$.

**Adım 3 — İadesiz.** Hiç premium olmayan seçimler $\binom{7}{3} = 35$, bütün seçimler $\binom{10}{3} = 120$:

$$
1 - \frac{35}{120} = \frac{85}{120} = \frac{17}{24} \approx 0{,}708
$$

**Sağlama:** Tam $0$, $1$, $2$, $3$ premium: $0{,}343 + 0{,}441 + 0{,}189 + 0{,}027 = 1$ ✓.

**Dikkat:** İkinci soruda $3$ ile çarpmayı unutmak yalnızca "ilki premium, ötekiler değil" sırasını sayar.

**Cevap:** $0{,}657$; $0{,}441$; $\frac{17}{24}$.
