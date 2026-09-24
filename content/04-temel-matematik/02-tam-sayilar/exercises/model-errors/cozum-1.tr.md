**Ne soruluyor?** İşaretli hatalar ve bunları üç farklı biçimde toplamak.

**Fikir:** Hata $e = y - \hat{y}$ işaretli bir sayı: model fazla tahmin ettiyse negatif, az tahmin ettiyse pozitif. Üç toplamın farkı, işaretlerin nasıl ele alındığında.

**Adım 1 — Hatalar.**

$$
\begin{aligned}
e_1 &= 10 - 13 = -3 \\
e_2 &= 7 - 6 = 1 \\
e_3 &= 12 - 9 = 3 \\
e_4 &= 5 - 8 = -3
\end{aligned}
$$

**Adım 2 — Hataların toplamı.** Pozitifler $1 + 3 = 4$, negatifler $-3 + (-3) = -6$:

$$
4 + (-6) = -2
$$

**Adım 3 — Mutlak değerlerin toplamı.**

$$
3 + 1 + 3 + 3 = 10
$$

**Adım 4 — Karelerin toplamı.**

$$
(-3)^2 + 1^2 + 3^2 + (-3)^2 = 9 + 1 + 9 + 9 = 28
$$

**Sonucu yorumla:** Toplam hata $-2$, sanki model neredeyse hiç yanılmıyormuş gibi gösteriyor; oysa her evde $1$ ile $3$ bin arasında hata var. Mutlak değer ve kare, pozitif ve negatif hataların birbirini götürmesini engelliyor. Kare, büyük hataları daha çok cezalandırıyor: $3$'lük hata $9$ sayılırken $1$'lik hata $1$ sayılıyor.

**Cevap:** $-2$, $10$ ve $28$.
