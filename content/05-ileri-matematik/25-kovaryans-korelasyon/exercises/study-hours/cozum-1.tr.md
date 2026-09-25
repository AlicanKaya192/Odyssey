**Ne soruluyor?** Küçük bir veride kovaryans, korelasyon ve birim değişikliğinin etkisi.

**Fikir:** Ortalamalardan sapmaların çarpımlarının ortalaması ($n - 1$ ile).

**Adım 1 — Kovaryans.** $\bar{x} = 5$, $\bar{y} = 68$. Sapmalar: $x$ için $-3, -2, 0, 1, 4$; $y$ için $-18, -8, -3, 7, 22$. Çarpımlar $54, 16, 0, 7, 88$; toplam $165$. $s_{xy} = \frac{165}{4} = 41{,}25$.

**Adım 2 — Korelasyon.** $s_x^2 = \frac{9 + 4 + 0 + 1 + 16}{4} = 7{,}5$, $s_y^2 = \frac{324 + 64 + 9 + 49 + 484}{4} = 232{,}5$.

$$
r = \frac{41{,}25}{\sqrt{7{,}5 \cdot 232{,}5}} = \frac{41{,}25}{41{,}76} \approx 0{,}988
$$

**Adım 3 — Dakika.** $x$ $60$ ile çarpılınca kovaryans da $60$ ile çarpılır: $41{,}25 \cdot 60 = 2475$. $r$ değişmez.

**Sağlama:** Bütün çarpımlar sıfır ya da pozitif; noktalar artan bir doğruya çok yakın, $r$'nin $1$'e yakın çıkması tutarlı ✓.

**Dikkat:** $n$ ile bölmek $33$ verir; örneklemde $n - 1$ kullanılır. $r$ ise ikisinde de aynı çıkar, çünkü bölen sadeleşir.

**Cevap:** $41{,}25$; $\approx 0{,}988$; $2475$.
