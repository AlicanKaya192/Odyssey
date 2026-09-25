**Ne soruluyor?** Küçük bir ağda kaybın çıktı ve ilk katman ağırlıklarına göre türevleri.

**Fikir:** Kayıptan başla; her katmanda gelen gradyanı ağırlıklarla geri taşı, ağırlık türevini girdiyle çarparak bul.

**Adım 1 — İleri.** $z_1 = 1$, $z_2 = -1 + 2 = 1$; $a = (1, 1)$; $\hat{y} = 2 - 1 = 1$; $L = 2$.

**Adım 2 — Çıktı.** $\frac{\partial L}{\partial \hat{y}} = -2$. $\frac{\partial L}{\partial w_{21}} = -2 \cdot a_1 = -2$.

**Adım 3 — Gizli katmana.** $\frac{\partial L}{\partial a} = -2 \cdot (2, -1) = (-4, 2)$. İki $z$ de pozitif: $\frac{\partial L}{\partial z} = (-4, 2)$.

**Adım 4 — İlk katman ağırlıkları.** $\frac{\partial L}{\partial W_{1j}} = \frac{\partial L}{\partial z_j} \cdot x$: $-4$ ve $2$.

**Sağlama:** $W_{11}$'i $0{,}01$ artır: $z_1 = 1{,}01$, $\hat{y} = 2{,}02 - 1 = 1{,}02$, $L = \frac{1}{2}(1{,}98)^2 = 1{,}9602$; değişim $-0{,}0398 / 0{,}01 \approx -3{,}98$ ✓.

**Dikkat:** İkinci gizli nöronun ağırlığı $w_{22} = -1$ negatif; bu yüzden ona giden gradyan pozitif ($+2$). İşareti kaçırmak $W_{12}$'yi $-2$ bulur.

**Cevap:** $-2$, $-4$ ve $2$.
