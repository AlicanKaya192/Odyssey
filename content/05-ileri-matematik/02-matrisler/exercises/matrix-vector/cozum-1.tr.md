**Ne soruluyor?** $A$ matrisini $\mathbf{x}$ vektörüyle çarpınca çıkan vektör.

**Fikir:** Önce boyutlara bak: $A$ $2 \times 3$ (2 satır, 3 sütun), $\mathbf{x}$ 3 bileşenli. Sütun sayısı vektörün boyuyla aynı olduğu için çarpım tanımlı. Sonuç, $A$'nın satır sayısı kadar, yani **2 bileşenli**.

Sonucun her bileşeni, $A$'nın bir satırı ile $\mathbf{x}$'in nokta çarpımı (satır bakışı): karşılıklı sayıları çarp, topla.

**Adım 1 — 1. satır.** $(1, -2, 0)$ ile $(4, 1, -1)$:

$$
\begin{aligned}
1 \cdot 4 + (-2) \cdot 1 + 0 \cdot (-1) &= 4 - 2 + 0 \\
&= 2
\end{aligned}
$$

**Adım 2 — 2. satır.** $(3, 1, 2)$ ile $(4, 1, -1)$:

$$
\begin{aligned}
3 \cdot 4 + 1 \cdot 1 + 2 \cdot (-1) &= 12 + 1 - 2 \\
&= 11
\end{aligned}
$$

**Adım 3 — Sonucu yaz.** 1. satırın sonucu üst bileşen, 2. satırınki alt bileşen:

$$
A\mathbf{x} = \begin{bmatrix} 2 \\ 11 \end{bmatrix}
$$

**Dikkat:** Sonuç 3 değil 2 bileşenli. Çıkan vektörün boyu matrisin satır sayısı kadar; sütun sayısı yalnızca çarpımın tanımlı olup olmadığını belirliyor.

**Cevap:** $A\mathbf{x} = (2, 11)$.
