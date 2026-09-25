**Fikir:** Üsleri eşitlemek yerine tekrar eden kuvveti yeni bir harfle adlandırmak. Birinci denklemde bunu gösterelim; öteki ikisi aynı yoldan çıkar.

**Adım 1 — Ayır.** $2^{x + 3} = 8 \cdot 2^x$ ve $4^{x - 1} = \frac{4^x}{4} = \frac{(2^x)^2}{4}$.

**Adım 2 — $u = 2^x$ de.** Denklem $8u = \frac{u^2}{4}$ olur, yani $u^2 = 32u$. $u = 2^x > 0$ olduğu için $u$'ya bölebiliriz: $u = 32$.

**Adım 3 — Geri dön.** $2^x = 32 = 2^5$, $x = 5$.

**Öteki iki denklem.** $u = 3^x$ ile ikincisi $u^3 = 81 u^2$, yani $u = 81 = 3^4$, $x = 4$. $u = 2^x$ ile üçüncüsü $\frac{1}{u} = \frac{u^3}{4096}$, yani $u^4 = 4096 = 2^{12}$, $u = 8$, $x = 3$.

**Neden aynı sonuç?** Değişken değiştirme, üs kurallarını ($b^{m + n} = b^m b^n$) üsse değil tabana uygulamak; sonunda yine "aynı taban, aynı üs" adımına varıyoruz. Bu yol, $4^x - 3 \cdot 2^x - 4 = 0$ gibi üsleri doğrudan eşitlenemeyen denklemlerde tek yol olur.

**Cevap:** $5$, $4$ ve $3$.
