**Fikir:** Elemenin sırası serbest; hangi bilinmeyeni önce yok edeceğini denklemlere bakarak seçebilirsin. Burada $z$'nin katsayıları $+1, +1, -1$: 3. denklemi öteki ikisine eklersek $z$ bir hamlede gidiyor ve iki bilinmeyenli bir sistem kalıyor.

**Adım 1 — 1. ve 3. denklemi topla.**

$$
\begin{aligned}
(x + y + z) + (x + 2y - z) &= 4 + (-3) \\
2x + 3y &= 1
\end{aligned}
$$

**Adım 2 — 2. ve 3. denklemi topla.**

$$
\begin{aligned}
(2x - y + z) + (x + 2y - z) &= 8 + (-3) \\
3x + y &= 5
\end{aligned}
$$

**Adım 3 — İki bilinmeyenli sistemi çöz.** İkinciden $y = 5 - 3x$. Birinciye koy:

$$
\begin{aligned}
2x + 3(5 - 3x) &= 1 \\
2x + 15 - 9x &= 1 \\
-7x &= -14 \\
x &= 2
\end{aligned}
$$

ve $y = 5 - 3 \cdot 2 = -1$.

**Adım 4 — $z$'yi bul.** 1. denklemden: $2 + (-1) + z = 4$, yani $z = 3$.

**Neden aynı sonuç?** Denklemleri toplamak da bir satır işlemi ($R_1 \to R_1 + R_3$). Gauss eleme sütunları soldan sağa sırayla temizliyor; biz yalnızca sırayı değiştirdik, önce $z$'nin sütununu temizledik. Satır işlemleri çözümü değiştirmediği için hangi sırayla yapılırsa yapılsın aynı yere varılır.

**Cevap:** $(2, -1, 3)$.
