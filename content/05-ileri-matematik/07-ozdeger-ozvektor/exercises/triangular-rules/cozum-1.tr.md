**Ne soruluyor?** Üç özdeğeri tek tek hesaplamadan onlarla ilgili üç bilgi.

**Fikir:** Üçgen bir matriste $A - \lambda I$ da üçgen; determinantı köşegen çarpımı. Öyleyse $\det(A - \lambda I) = (2 - \lambda)(3 - \lambda)(-1 - \lambda)$ ve özdeğerler doğrudan köşegen elemanları.

**Adım 1 — Özdeğerler.** Köşegen: $2$, $3$, $-1$. Köşegenin üstündeki $1, 4, 5$ özdeğerleri etkilemiyor.

**Adım 2 — Toplam.**

$$
2 + 3 + (-1) = 4
$$

Sağlama: iz $= 2 + 3 - 1 = 4$ ✓ (toplam her zaman ize eşit).

**Adım 3 — Çarpım.**

$$
2 \cdot 3 \cdot (-1) = -6
$$

Sağlama: üçgen matrisin determinantı da köşegen çarpımı, $-6$ ✓.

**Adım 4 — $A^2$'nin özdeğerleri.** Kuvvet kuralı: $A\mathbf{v} = \lambda\mathbf{v}$ ise $A^2\mathbf{v} = \lambda^2\mathbf{v}$. Kareler:

$$
2^2 = 4, \qquad 3^2 = 9, \qquad (-1)^2 = 1
$$

En büyüğü $9$.

**Dikkat:** $A^2$'yi hesaplayıp köşegenine bakmak da işe yarar (üçgen matrisin karesi yine üçgen, köşegeni $4, 9, 1$), ama kural bunu tek satırda veriyor.

**Cevap:** $4$, $-6$, $9$.
