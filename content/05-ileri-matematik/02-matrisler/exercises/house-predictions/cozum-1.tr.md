**Ne soruluyor?** Model her ev için bir fiyat tahmin ediyor: her özelliği kendi ağırlığıyla çarpıp topluyor, sonuna da sabit $b$'yi ekliyor. Üç evin üçü için bu hesabı yapacağız.

**Fikir:** $X\mathbf{w}$'nin her bileşeni, $X$'in bir satırı ile $\mathbf{w}$'nin nokta çarpımı (satır bakışı). $X$'in her satırı bir ev olduğu için her nokta çarpımı bir evin tahmini. Ağırlıkların anlamı:

- Alan: yüz metrekare başına $+100$ bin lira.
- Oda: oda başına $+20$ bin lira.
- Yaş: yıl başına $-2$ bin lira (ev eskidikçe ucuzluyor).

**Adım 1 — 1. ev** (1. satır: $1.2$, $3$, $10$). Her özelliği ağırlığıyla çarp, topla, $10$ ekle:

$$
\begin{aligned}
\hat{y}_1 &= 1.2 \cdot 100 + 3 \cdot 20 + 10 \cdot (-2) + 10 \\
&= 120 + 60 - 20 + 10 \\
&= 170
\end{aligned}
$$

**Adım 2 — 2. ev** (2. satır: $0.8$, $2$, $25$):

$$
\begin{aligned}
\hat{y}_2 &= 0.8 \cdot 100 + 2 \cdot 20 + 25 \cdot (-2) + 10 \\
&= 80 + 40 - 50 + 10 \\
&= 80
\end{aligned}
$$

**Adım 3 — 3. ev** (3. satır: $1.5$, $4$, $5$):

$$
\begin{aligned}
\hat{y}_3 &= 1.5 \cdot 100 + 4 \cdot 20 + 5 \cdot (-2) + 10 \\
&= 150 + 80 - 10 + 10 \\
&= 230
\end{aligned}
$$

**Sonucu yorumla:** En pahalısı 3. ev (en büyük, en çok odalı, en yeni). En ucuzu 2. ev: hem küçük hem 25 yaşında.

**Dikkat:** $b$ her tahmine ayrı ayrı eklenir; yalnızca birine değil.

**Cevap:** $170$, $80$, $230$.
