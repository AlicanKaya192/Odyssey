**Ne soruluyor?** Eğitim verisinden hesaplanan ölçekleme değerlerinin test verisine uygulanması.

**Fikir:** Ortalama, standart sapma, en küçük ve en büyük **yalnızca eğitimden** hesaplanır; test değerleri aynı sayılarla dönüştürülür.

**Adım 1 — Standart sapma.** Ortalama $30$. Sapmaların kareleri $400, 100, 0, 100, 400$; toplam $1000$; varyans $200$.

$$
\sigma = \sqrt{200} = 10\sqrt{2} \approx 14{,}142
$$

**Adım 2 — $45$'in z puanı.** $\frac{45 - 30}{14{,}142} \approx 1{,}061$.

**Adım 3 — $60$'ın min–maks değeri.** $\frac{60 - 10}{50 - 10} = \frac{50}{40} = 1{,}25$.

**Sağlama:** Eğitim değerleri min–maks ile $0; 0{,}25; 0{,}5; 0{,}75; 1$ olur. $60$ eğitimdeki en büyükten büyük olduğu için $1$'i geçmesi doğal ✓.

**Dikkat:** $60$'ı görünce en büyüğü $60$ yapıp yeniden hesaplamak test verisinden bilgi sızdırmak olur. Ölçekleme sayıları eğitimde bir kez belirlenir ve değişmez; test değerleri $[0, 1]$ dışına çıkabilir.

**Cevap:** $14{,}142$; $1{,}061$; $1{,}25$.
