**Ne soruluyor?** Nadir bir sınıfta iyi bir modelin alarmlarının ne kadarının doğru olduğu.

**Fikir:** Oranları işlem sayısına çevir; kesinlik, gerçek alarmların bütün alarmlar içindeki payı.

**Adım 1 — Gruplar.** Dolandırıcılık $100\,000 \cdot 0{,}002 = 200$; normal $99\,800$.

**Adım 2 — Alarmlar.** Gerçek: $200 \cdot 0{,}95 = 190$. Yanlış: $99\,800 \cdot 0{,}01 = 998$. Toplam $1188$.

**Adım 3 — Kesinlik.** $\frac{190}{1188} \approx 0{,}160$.

**Sağlama:** Bayes kuralıyla $\frac{0{,}95 \cdot 0{,}002}{0{,}95 \cdot 0{,}002 + 0{,}01 \cdot 0{,}998} \approx 0{,}160$ ✓.

**Dikkat:** Modelin "yüzde $95$ yakalıyor, yüzde $99$ doğru" olması alarmların çoğunun doğru olduğunu göstermez; her $6$ alarmdan $5$'i yanlış. Doğruluk da yanıltır: model $100\,000$ işlemden $190 + 98\,802 = 98\,992$'sini doğru sınıflıyor, yani yaklaşık yüzde $99$.

**Cevap:** $1188$; $190$; $\approx 0{,}160$.
