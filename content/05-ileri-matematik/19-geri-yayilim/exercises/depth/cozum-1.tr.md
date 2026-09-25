**Ne soruluyor?** Katmanlar boyunca çarpılan türevlerin sönme ve patlama hızı.

**Fikir:** $n$ katmandan sonra çarpım çarpanın $n$'inci kuvveti.

**Adım 1 — Beş katman.** $0{,}25^5 = \frac{1}{4^5} = \frac{1}{1024} \approx 0{,}000977$.

**Adım 2 — Eşik.** $4^4 = 256 < 1000$, $4^5 = 1024 > 1000$: $n = 5$ ilk kez $0{,}001$'in altına iniyor.

**Adım 3 — Patlama.** $1{,}1^{50} = e^{50 \cdot 0{,}09531} = e^{4{,}7655} \approx 117{,}4$.

**Sağlama:** $1{,}1^{10} \approx 2{,}594$; $2{,}594^5 \approx 117{,}4$ ✓.

**Dikkat:** Çarpanın $1$'den küçücük farkları bile derinlikte katlanıyor; $0{,}9^{50} \approx 0{,}005$, $1{,}1^{50} \approx 117$. İyi başlangıç yöntemlerinin çarpanı tam $1$ civarında tutmaya çalışmasının nedeni bu.

**Cevap:** $\frac{1}{1024}$, $5$ ve $\approx 117{,}4$.
