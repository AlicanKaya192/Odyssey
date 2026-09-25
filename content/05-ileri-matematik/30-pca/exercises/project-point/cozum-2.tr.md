**Fikir:** Merkezlenmiş vektör, bileşen yönündeki parça ile ona dik parçanın toplamı: $\lVert x - \bar{x}\rVert^2 = z_1^2 + \lVert\text{hata}\rVert^2$.

**Adım 1 — Skor.** $z_1 = 2\sqrt{2}$, $z_1^2 = 8$.

**Adım 2 — Geri çatma.** $\bar{x} + z_1u_1$; birinci koordinat $2 + 2\sqrt{2} \cdot \frac{1}{\sqrt{2}} = 4$.

**Adım 3 — Hata.** $\lVert(3, 1)\rVert^2 = 10$; hata $10 - 8 = 2$.

**Neden aynı sonuç?** Geri çatma dik izdüşüm olduğu için hata vektörü izdüşüme dik; dik iki vektörün toplamında Pisagor geçerli. PCA'nın "varyansı en büyük yap" ile "hatayı en küçük yap" bakışlarının denkliği de bu eşitlikten geliyor.

**Cevap:** $2{,}828$; $4$ ve $2$.
