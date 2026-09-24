**Ne soruluyor?** İki iç içe fonksiyonun türevinin $x = 1$'deki değeri.

**Fikir:** Zincir kuralı: dıştakinin türevi (içi aynen kalarak) çarpı içtekinin türevi.

**Adım 1 — $y'$.** $y' = 4(2x^2 - 3)^3 \cdot 4x = 16x(2x^2 - 3)^3$.

**Adım 2 — $y'(1)$.** $16 \cdot 1 \cdot (-1)^3 = -16$.

**Adım 3 — $z'$.** $z' = e^{-x^2/2} \cdot (-x)$; $z'(1) = -e^{-1/2} \approx -0{,}6065 \approx -0{,}607$.

**Sağlama:** $x = 1$'de $2x^2 - 3 = -1$; $y$'nin $1$ çevresindeki değerleri: $y(1{,}01) = (-0{,}9598)^4 \approx 0{,}8486$, $y(0{,}99) = (-1{,}0398)^4 \approx 1{,}1690$. Fark bölü $0{,}02$: $\approx -16{,}0$ ✓.

**Dikkat:** İçtekinin türevini unutmak $y' = 4(2x^2 - 3)^3$ verir, $x = 1$'de $-4$; dört kat küçük.

**Cevap:** $y'(1) = -16$, $z'(1) \approx -0{,}607$.
