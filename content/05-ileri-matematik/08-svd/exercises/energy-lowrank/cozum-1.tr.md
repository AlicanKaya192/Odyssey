**Ne soruluyor?** İlk iki katmanı tutup son ikisini atınca matrisin ne kadarının kaldığı ve ne kadar hata yapıldığı.

**Fikir:** $A = \sum \sigma_i\mathbf{u}_i\mathbf{v}_i^\mathsf{T}$. Rankı 2 olan en iyi yaklaşım ilk iki katman (Eckart–Young). Elemanların kareleri toplamı $\sum \sigma_i^2$; bu yüzden "enerji" kareler üzerinden hesaplanır ve atılan kısmın hatası atılan karelerden gelir.

**Adım 1 — Kareler.**

$$
\begin{aligned}
\sigma_1^2 &= 144 \\
\sigma_2^2 &= 25 \\
\sigma_3^2 &= 9 \\
\sigma_4^2 &= 1
\end{aligned}
$$

Toplam enerji $179$.

**Adım 2 — Korunan pay.**

$$
\frac{144 + 25}{179} = \frac{169}{179} \approx 0.944
$$

**Adım 3 — Hata.** Atılan katmanlar $\sigma_3$ ve $\sigma_4$:

$$
\begin{aligned}
\|A - A_2\| &= \sqrt{\sigma_3^2 + \sigma_4^2} \\
&= \sqrt{9 + 1} = \sqrt{10} \approx 3.16
\end{aligned}
$$

**Sağlama:** Korunan ve atılan enerji toplamı: $169 + 10 = 179$ ✓.

**Dikkat:** Tekil değerlerin kendisiyle oran almak ($\tfrac{12 + 5}{21} \approx 0.81$) yanlış; karelerle hesaplanır. Kare, küçük tekil değerlerin payını daha da küçültüyor: burada iki katman matrisin %94'ünü taşıyor.

**Cevap:** $0.94$ ve $3.16$.
