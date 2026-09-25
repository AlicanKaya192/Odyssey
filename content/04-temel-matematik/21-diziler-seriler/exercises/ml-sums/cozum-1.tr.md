**Ne soruluyor?** Bir hata fonksiyonunun değeri, indirgenmiş sonsuz ödül ve hareketli ortalama ağırlıklarının bir kısmi toplamı.

**Fikir:** Üçü de birer Σ. İlki sonlu bir toplam, ikincisi sonsuz geometrik seri, üçüncüsü sonlu geometrik seri.

**Adım 1 — MSE.** Farklar $y_i - \hat{y}_i$: $-1, 0, 2, -1$. Kareler $1, 0, 4, 1$; toplam $6$.

$$
\text{MSE} = \frac{6}{4} = 1{,}5
$$

**Adım 2 — İndirgenmiş ödül.** $a_1 = 2$, $r = 0{,}8$:

$$
2 + 1{,}6 + 1{,}28 + \dots = \frac{2}{1 - 0{,}8} = 10
$$

**Adım 3 — Ağırlıklar.** $0{,}5$; $0{,}25$; $0{,}125$. Toplam $0{,}875$.

**Sağlama:** Üçüncüde formül: $0{,}5 \cdot \frac{1 - 0{,}5^3}{1 - 0{,}5} = 1 - 0{,}125 = 0{,}875$ ✓.

**Dikkat:** MSE'de farkların karesi alınmadan toplanırsa $-1 + 0 + 2 - 1 = 0$ çıkar: artı ve eksi hatalar birbirini götürür. Kare bu yüzden var.

**Cevap:** $1{,}5$, $10$, $0{,}875$.
