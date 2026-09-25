**Ne soruluyor?** Bir karar ağacı bölmesinin entropiyi ne kadar düşürdüğü.

**Fikir:** Kazanç $= H(\text{ebeveyn}) - \left[\frac{6}{16}H(\text{sol}) + \frac{10}{16}H(\text{sağ})\right]$.

**Adım 1 — Sol.** $-\log_2\frac{5}{6} = \log_2 6 - \log_2 5 \approx 0{,}263$; $-\log_2\frac{1}{6} \approx 2{,}585$. $H \approx \frac{5}{6} \cdot 0{,}263 + \frac{1}{6} \cdot 2{,}585 \approx 0{,}219 + 0{,}431 = 0{,}650$.

**Adım 2 — Sağ ve ortalama.** $-\log_2 0{,}3 = \log_2 10 - \log_2 3 \approx 1{,}737$; $-\log_2 0{,}7 \approx 0{,}515$. $H \approx 0{,}3 \cdot 1{,}737 + 0{,}7 \cdot 0{,}515 \approx 0{,}881$. Ağırlıklı: $0{,}375 \cdot 0{,}650 + 0{,}625 \cdot 0{,}881 \approx 0{,}795$.

**Adım 3 — Kazanç.** $1 - 0{,}795 = 0{,}205$ bit.

**Sağlama:** Kazanç $0$ ile $1$ arasında ✓; iki çocuk da ebeveynden daha saf ✓.

**Dikkat:** Çocukların entropilerini ağırlıksız ortalamak ($\frac{0{,}650 + 0{,}881}{2} = 0{,}766$) büyük grubun etkisini küçük gösterir.

**Cevap:** $\approx 0{,}650$; $\approx 0{,}795$; $\approx 0{,}205$.
