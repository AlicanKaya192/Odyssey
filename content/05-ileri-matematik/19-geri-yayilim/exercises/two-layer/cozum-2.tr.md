**Fikir:** Ağ küçük; $\hat{y}$'yi ağırlıkların açık bir fonksiyonu olarak yaz. Noktanın yakınında iki $z$ de pozitif, ReLU etkisiz.

**Adım 1 — Açık biçim.** $\hat{y} = w_{21}(W_{11}x) + w_{22}(W_{12}x + 2)$.

**Adım 2 — Zincir.** $\frac{\partial L}{\partial \theta} = (\hat{y} - y) \frac{\partial \hat{y}}{\partial \theta} = -2 \frac{\partial \hat{y}}{\partial \theta}$.

**Adım 3 — Türevler.** $\frac{\partial \hat{y}}{\partial w_{21}} = W_{11}x = 1$: $-2$. $\frac{\partial \hat{y}}{\partial W_{11}} = w_{21}x = 2$: $-4$. $\frac{\partial \hat{y}}{\partial W_{12}} = w_{22}x = -1$: $2$.

**Neden aynı sonuç?** Geri yayılım bu çarpımları ($w_{21} \cdot x$ gibi) katman katman, ortak parçaları ($\frac{\partial L}{\partial \hat{y}} = -2$) bir kez hesaplayarak kuruyor. Açık yazım burada mümkün; on katmanlı bir ağda terim sayısı patlar, geri yayılımın maliyeti ise katman sayısıyla doğrusal büyür.

**Cevap:** $-2$, $-4$, $2$.
