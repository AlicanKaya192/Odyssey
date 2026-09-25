**Fikir:** Hata payı $\frac{z^{*}}{\sqrt{n}}$ ile orantılı. Bilinen bir noktadan ($n = 100$, $E = 3{,}92$) oranla ilerle.

**Adım 1 — Başlangıç.** $n = 100$'de $3{,}92$.

**Adım 2 — Yüzde 95, $E = 2$.** Hata payını $\frac{3{,}92}{2} = 1{,}96$ kat küçültmek için $n$ $1{,}96^2 = 3{,}8416$ kat: $384{,}16$, yani $385$.

**Adım 3 — Yüzde 99.** $z^{*}$ $\frac{2{,}576}{1{,}96}$ kat büyüyor; aynı hata payını korumak için $n$ bu oranın karesi kadar, $1{,}7274$ kat büyümeli: $384{,}16 \cdot 1{,}7274 \approx 663{,}6$, yani $664$.

**Neden aynı sonuç?** $n$, $(z^{*})^2$ ile doğru, $E^2$ ile ters orantılı; oranlarla ilerlemek formülü parça parça uygulamaktır.

**Cevap:** $3{,}92$; $385$ ve $664$.
