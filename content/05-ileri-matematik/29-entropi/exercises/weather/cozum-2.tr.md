**Fikir:** Entropi, sonucu bulmak için gereken ortalama evet–hayır soru sayısı (en iyi stratejide).

**Adım 1 — Sorular.** Önce "güneşli mi?" diye sor: yarı yarıya tek soruda biter. Değilse "bulutlu mu?": $2$ soru. Ortalama $\frac{1}{2} \cdot 1 + \frac{1}{2} \cdot 2 = 1{,}5$.

**Adım 2 — Nat.** Aynı bilgi doğal logaritmayla: $\frac{1}{2}\ln 2 + \frac{1}{2}\ln 4 = 1{,}5\ln 2 \approx 1{,}040$.

**Adım 3 — Üst sınır.** Üç eşit sonuçta en iyi strateji bile ortalama $\frac{5}{3} \approx 1{,}667$ soru ister; entropi $\log_2 3 \approx 1{,}585$ bundan biraz az, çünkü tam sayı soru kısıtı yok (çok sayıda sonuç birlikte kodlanınca bu sınıra yaklaşılır).

**Neden aynı sonuç?** Olasılıklar $2$'nin kuvvetleri olunca en iyi soru ağacının dallarının uzunlukları tam olarak $-\log_2 p$ olur; ortalama soru sayısı entropiye eşit çıkar.

**Cevap:** $1{,}5$; $1{,}040$ ve $1{,}585$.
