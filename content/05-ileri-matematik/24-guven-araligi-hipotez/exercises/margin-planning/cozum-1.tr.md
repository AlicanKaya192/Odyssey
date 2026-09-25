**Ne soruluyor?** Hata payı ve istenen hata payı için gereken örneklem büyüklüğü.

**Fikir:** $E = z^{*}\frac{\sigma}{\sqrt{n}}$; $n$ için çözülünce $n = \left(\frac{z^{*}\sigma}{E}\right)^2$.

**Adım 1 — $n = 100$.** $1{,}96 \cdot \frac{20}{10} = 3{,}92$.

**Adım 2 — Yüzde 95.** $\left(\frac{1{,}96 \cdot 20}{2}\right)^2 = 19{,}6^2 = 384{,}16$; yukarı yuvarla: $385$.

**Adım 3 — Yüzde 99.** $\left(\frac{2{,}576 \cdot 20}{2}\right)^2 = 25{,}76^2 = 663{,}58$; yukarı yuvarla: $664$.

**Sağlama:** $385$ gözlemle hata payı $1{,}96 \cdot \frac{20}{\sqrt{385}} \approx 1{,}998 \leq 2$ ✓; $384$ ile $\approx 2{,}0004$, biraz fazla.

**Dikkat:** $384{,}16$'yı $384$'e yuvarlamak hata payını sınırın üstüne çıkarır; "en az" soruluyorsa hep yukarı.

**Cevap:** $3{,}92$; $385$; $664$.
