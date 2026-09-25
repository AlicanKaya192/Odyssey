**Fikir:** $n$ gözlemde $k$ başarı için $\hat{p} = \frac{k}{n}$; $\ell(\hat{p}) = n\big[\hat{p}\ln\hat{p} + (1 - \hat{p})\ln(1 - \hat{p})\big]$ ve $\ell'(p) = \frac{n(\hat{p} - p)}{p(1 - p)}$.

**Adım 1 — MLE.** $\frac{8}{200} = 0{,}04$.

**Adım 2 — $\ell(\hat{p})$.** $200 \cdot \big[0{,}04 \cdot (-3{,}2189) + 0{,}96 \cdot (-0{,}0408)\big] = 200 \cdot (-0{,}1679) \approx -33{,}59$.

**Adım 3 — $\ell'(0{,}05)$.** $\frac{200 \cdot (0{,}04 - 0{,}05)}{0{,}05 \cdot 0{,}95} = \frac{-2}{0{,}0475} \approx -42{,}11$.

**Neden aynı sonuç?** $\frac{k}{p} - \frac{n - k}{1 - p}$ ortak paydada $\frac{k - np}{p(1 - p)}$ olur ve $k = n\hat{p}$; ikinci formül birincinin sadeleşmiş hâli. Köşeli parantezdeki ifade, Entropi bölümünde göreceğimiz entropinin eksi işaretlisi.

**Cevap:** $0{,}04$; $-33{,}59$ ve $-42{,}11$.
