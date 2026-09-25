**Fikir:** Entropi bir beklenen değer: $H = E[I(X)]$. Önce her sonucun bilgisini bul, sonra olasılıklarla ortala.

**Adım 1 — Tura.** $I = 3{,}322$ bit ($\frac{1}{10}$'luk bir olay; $\frac{1}{8}$ olsaydı tam $3$ bit olurdu).

**Adım 2 — Yazı.** $I = 0{,}152$ bit.

**Adım 3 — Beklenen değer.** $E[I] = 0{,}9 \cdot 0{,}152 + 0{,}1 \cdot 3{,}322 \approx 0{,}469$.

**Neden aynı sonuç?** $-\sum p\log_2 p = \sum p \cdot (-\log_2 p) = \sum p \cdot I$; entropi formülü tam olarak bilginin beklenen değeri. Nadir sonucun büyük bilgisi, küçük olasılığıyla çarpıldığı için entropiyi az etkiliyor.

**Cevap:** $0{,}469$; $3{,}322$ ve $0{,}152$.
