**Ne soruluyor?** İki modelin doğruluk farkının rastgele dalgalanmaya göre ne kadar büyük olduğu.

**Fikir:** Her doğruluk bir örneklem oranı; bağımsız iki test setinde farkın varyansı, iki varyansın toplamı.

**Adım 1 — A.** $\sqrt{\frac{0{,}88 \cdot 0{,}12}{1000}} = \sqrt{0{,}0001056} \approx 0{,}0103$.

**Adım 2 — Fark.** B için $\sqrt{\frac{0{,}9 \cdot 0{,}1}{1000}} \approx 0{,}0095$. Farkın standart hatası $\sqrt{0{,}0001056 + 0{,}00009} \approx 0{,}0140$.

**Adım 3 — $z$.** $\frac{0{,}02}{0{,}0140} \approx 1{,}43$.

**Sağlama:** Farkın standart hatası iki standart hatanın toplamından ($0{,}0198$) küçük, ikisinin büyüğünden ($0{,}0103$) büyük ✓.

**Dikkat:** $1{,}43$ standart hata, iki standart hatanın altında: fark yüzde $2$ olsa da rastgele dalgalanmayla açıklanabilir. "B daha iyi" demek için daha çok test verisi gerekir.

**Cevap:** $\approx 0{,}0103$; $\approx 0{,}0140$; $\approx 1{,}43$.
