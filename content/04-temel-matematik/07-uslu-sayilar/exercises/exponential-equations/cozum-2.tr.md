**Fikir:** Küçük tam sayıları dene. $2^x = 32$ gibi denklemlerde tam sayı cevap hemen çıkar; $9^y = 27$'de ise cevabın iki tam sayı arasında kaldığını görür, sonra onu yakalarız.

**Adım 1 — $2^x$'i dene.** $2^1 = 2$, $2^2 = 4$, $2^3 = 8$, $2^4 = 16$, $2^5 = 32$ ✓. $x = 5$.

**Adım 2 — $9^y$'yi dene.** $9^1 = 9 < 27 < 81 = 9^2$: cevap $1$ ile $2$ arasında, tam sayı değil.

**Adım 3 — $27$'yi $9$ cinsinden yaz.** $27 = 9 \cdot 3$ ve $3$, $9$'un "yarım kuvveti" ($3 \cdot 3 = 9$). Yani $27 = 9^1 \cdot 9^{1/2} = 9^{1 + 1/2}$.

**Adım 4 — Oku.** $y = 1 + \frac{1}{2} = \frac{3}{2}$.

**Neden aynı sonuç?** $3 = 9^{1/2}$ demek, $(3^2)^{1/2} = 3^1$ demek: birinci yoldaki $3^{2y} = 3^3$ eşitliğinin sözle anlatılışı. Deneme yolu cevabın $1$ ile $2$ arasında olduğunu gösterdiği için kesirli bir üs beklememiz gerektiğini de anlattı.

**Cevap:** $5$ ve $\dfrac{3}{2}$.
