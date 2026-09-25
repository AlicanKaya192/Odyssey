**Fikir:** Kutuları birim kareli kâğıda çiz ve kareleri say; alan birim kare sayısı.

**Adım 1 — Kutular.** Gerçek kutu $4$ sütun $\times$ $3$ satır $= 12$ kare. Tahmin $4$ sütun $\times$ $4$ satır $= 16$ kare.

**Adım 2 — Ortak kareler.** İki kutunun da içinde kalan kareler $x = 3$ ile $5$, $y = 2$ ile $4$ arasında: $2 \times 2 = 4$ kare.

**Adım 3 — Toplam kaplanan.** Yalnız gerçek kutuda $12 - 4 = 8$, yalnız tahminde $16 - 4 = 12$, ikisinde $4$: toplam $8 + 12 + 4 = 24$. $\text{IoU} = \frac{4}{24}$.

**Neden aynı sonuç?** "Yalnız A + yalnız B + ortak" sayımı, $A + B - \text{kesişim}$ formülünün açık hâli: $A + B$ ortak bölgeyi iki kez sayıyor, bir kez çıkarınca düzeliyor.

**Cevap:** $4$, $24$ ve $\frac{1}{6}$.
