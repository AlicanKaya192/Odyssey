**Ne soruluyor?** Hiç görülmemiş bir olayın MLE'si ve düzeltilmiş tahminler.

**Fikir:** MLE $\frac{k}{n}$; Laplace $\frac{k + 1}{n + 2}$.

**Adım 1 — MLE.** $\frac{0}{40} = 0$.

**Adım 2 — Spam, Laplace.** $\frac{0 + 1}{40 + 2} = \frac{1}{42} \approx 0{,}0238$.

**Adım 3 — Normal, Laplace.** $\frac{12 + 1}{60 + 2} = \frac{13}{62} \approx 0{,}210$. (MLE $0{,}2$ idi; çok veri olduğunda düzeltme az şey değiştirir.)

**Sağlama:** MLE ile bir e-postada "fatura" geçerse spam olabilirliği $0$ olur; diğer bütün kelimeler ne kadar spam gibi olursa olsun sonuç "normal" çıkar. Düzeltilmiş tahminle olabilirlik oranı $\frac{0{,}210}{0{,}0238} \approx 8{,}8$: güçlü ama mutlak olmayan bir kanıt ✓.

**Dikkat:** Laplace düzeltmesi az veride büyük, çok veride küçük etki yapar; spam tahmini $0$'dan $0{,}024$'e çıkarken normal tahmin yalnızca $0{,}2$'den $0{,}21$'e kaydı.

**Cevap:** $0$; $\approx 0{,}0238$; $\approx 0{,}210$.
