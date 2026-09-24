**Fikir:** Geri yayılımın yaptığı gibi: önce $L$'nin $z$'ye göre türevini, $\delta$'yı bir kez hesapla. Sonra her parametre $\delta$'yı kendi son halkasıyla çarpar.

**Adım 1 — $\delta$.** $\delta = \frac{\partial L}{\partial z} = 2(\hat{y} - y) \cdot \sigma'(z) = (-1)(0{,}25) = -0{,}25$.

**Adım 2 — Paylaştır.** $z = wx + b$: $\frac{\partial L}{\partial w} = \delta \cdot x = -0{,}5$; $\frac{\partial L}{\partial b} = \delta \cdot 1 = -0{,}25$.

**Adım 3 — Adım.** $w = 0 + 0{,}5 = 0{,}5$ (ve $b = 0{,}25$).

**Neden aynı sonuç?** Birinci yolda iki türev ayrı ayrı çarpılırken ilk iki halka ($-1$ ve $0{,}25$) iki kez yazıldı. $\delta$ o ortak kısmı bir kez hesaplıyor. Tek nöronda kazanç küçük; milyonlarca parametreli bir ağda geri yayılımı hızlı yapan tam olarak bu paylaşım.

**Cevap:** $-0{,}5$, $-0{,}25$ ve $0{,}5$.
