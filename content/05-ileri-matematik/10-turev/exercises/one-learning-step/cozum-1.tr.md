**Ne soruluyor?** Tek ağırlıklı bir modelde bir gradyan inişi adımı.

**Fikir:** Kaybın türevi, ağırlığı hangi yöne itmek gerektiğini söyler. Türevi bul, adımı at, yeni kaybı hesapla.

**Adım 1 — Türev.** $L(w) = 4w^2 - 24w + 36$, $L'(w) = 8w - 24$. $L'(1) = -16$.

**Adım 2 — Adım.**

$$
w \leftarrow 1 - 0{,}05 \cdot (-16) = 1 + 0{,}8 = 1{,}8
$$

**Adım 3 — Yeni kayıp.** $L(1{,}8) = (3{,}6 - 6)^2 = (-2{,}4)^2 = 5{,}76$.

**Sağlama:** Eski kayıp $L(1) = (2 - 6)^2 = 16$; yeni kayıp $5{,}76$. Kayıp düştü ✓. En iyi ağırlık $w = 3$ ($2 \cdot 3 = 6$); $w$ doğru yöne, $1$'den $1{,}8$'e gitti.

**Dikkat:** Eğim negatifken $\eta L'$'yi eklemek ($1 - 0{,}8 = 0{,}2$) ters yöne gider ve kaybı artırır; formüldeki eksi işareti "eğimin tersine" demek.

**Cevap:** $L'(1) = -16$, $w = 1{,}8$, kayıp $5{,}76$.
