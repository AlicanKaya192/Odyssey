**Fikir:** $2 \times 2$ için bildiğimiz formülle aynı sonucu bulup Gauss–Jordan'ın neden tuttuğunu görelim. İkisini karşılaştırmak iki yöntemin de doğru uygulandığını gösterir.

**Adım 1 — Determinant.**

$$
\det A = 1 \cdot 7 - 2 \cdot 3 = 7 - 6 = 1
$$

**Adım 2 — Yer değiştir, işaret çevir, $1$'e böl.** $1$ ile $7$ yer değiştiriyor; $2$ ve $3$'ün işareti dönüyor:

$$
A^{-1} = \frac{1}{1} \begin{bmatrix} 7 & -2 \\ -3 & 1 \end{bmatrix}
$$

**Adım 3 — Karşılaştır.** Gauss–Jordan'ın sağ tarafında bulduğumuz matrisle birebir aynı.

**Neden aynı?** Gauss–Jordan'da yaptığımız her işlem (burada $R_2 - 3R_1$ ve $R_1 - 2R_2$) bir matrisle soldan çarpmak demek. Bu matrislerin çarpımı $A$'yı $I$'ya çevirdiğine göre $A^{-1}$'in ta kendisi. Formül, bu işlemleri $a, b, c, d$ harfleriyle bir kez yapıp sonucu yazmanın kısa yolu; paydada çıkan $ad - bc$ de elemedeki pivotların çarpımı ($1 \cdot 1 = 1$).

**Ne zaman hangisi?** $2 \times 2$'de formül daha hızlı. $3 \times 3$ ve üstünde formül karmaşıklaşıyor; Gauss–Jordan her boyutta aynı adımlarla çalışıyor.

**Cevap:** $7$, $-2$, $-3$, $1$.
