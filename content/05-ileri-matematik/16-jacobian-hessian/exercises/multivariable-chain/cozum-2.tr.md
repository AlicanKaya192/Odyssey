**Fikir:** Ara değişkenleri yerine koyup $z$'yi doğrudan $t$'nin fonksiyonu olarak yaz, tek değişkenli türev al.

**Adım 1 — Yerine koy.** $z = (2t)^2 (t^2 + 1) = 4t^4 + 4t^2$.

**Adım 2 — Türev.** $\frac{dz}{dt} = 16t^3 + 8t$; $t = 1$'de $24$.

**Adım 3 — Kısmi türev.** $\frac{\partial z}{\partial x} = 2xy$; $(2, 2)$'de $8$.

**Neden aynı sonuç?** İki yolu açınca $2xy \cdot x' = 8t(t^2 + 1)$ ve $x^2 y' = 8t^3$; toplamları $16t^3 + 8t$. Yerine koymak iki yolu tek formülde birleştiriyor. Sinir ağlarında ise yerine koymak imkânsız (milyonlarca ara değişken), bu yüzden zincir kuralı yolları tek tek toplar.

**Cevap:** $24$ ve $8$.
