**Ne soruluyor?** Yarı ömrü bilinen bir miktarın belli bir süre sonraki değeri, belli bir değere inme süresi ve saatlik azalma çarpanı.

**Fikir:** Kalan miktar $N(t) = 240 \cdot \left( \frac{1}{2} \right)^{t / 4}$.

**Adım 1 — $12$ saat.** $\frac{12}{4} = 3$ yarı ömür:

$$
N(12) = 240 \cdot \left( \tfrac{1}{2} \right)^3 = \frac{240}{8} = 30
$$

**Adım 2 — $7{,}5$ mg.** $240 \cdot \left( \frac{1}{2} \right)^{t / 4} = 7{,}5$, yani $2^{t / 4} = \frac{240}{7{,}5} = 32 = 2^5$. Üsler eşit: $\frac{t}{4} = 5$, $t = 20$ saat.

**Adım 3 — Saatlik çarpan.** Dört saatte çarpan $\frac{1}{2}$; saatlik çarpan $c$ ise $c^4 = \frac{1}{2}$:

$$
c = \left( \tfrac{1}{2} \right)^{1/4} = \frac{1}{\sqrt[4]{2}} \approx 0{,}8409
$$

Yani her saat yaklaşık yüzde $15{,}9$ azalıyor.

**Sağlama:** $0{,}8409^4 \approx 0{,}5$ ✓.

**Dikkat:** Saatlik azalma yüzde $12{,}5$ değil ($50 / 4$); yüzdeler bölünmez, çarpan kök alınarak paylaştırılır.

**Cevap:** $30$ mg, $20$ saat, $0{,}8409$.
