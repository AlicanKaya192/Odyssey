**1. Çarpım kuralıyla birleştir:**

$$
\log_2 \big((x + 2)(x - 4)\big) = 4
$$

**2. Tanıma çevir** ($\log_2 A = 4 \iff A = 2^4$):

$$
(x + 2)(x - 4) = 16
$$

**3. Parantezi aç ve sıfıra eşitle:**

$$
x^2 - 4x + 2x - 8 = 16
\quad\Rightarrow\quad
x^2 - 2x - 24 = 0
$$

**4. Çarpanlarına ayır.** Çarpımı $-24$, toplamı $-2$ olan iki sayı: $-6$ ve $4$.

$$
(x - 6)(x + 4) = 0
\quad\Rightarrow\quad
x = 6 \;\text{ ya da }\; x = -4
$$

**5. Her adayı orijinal denklemde kontrol et:**

| Aday | $x + 2$ | $x - 4$ | Geçerli mi? |
|---|---|---|---|
| $x = 6$ | $8 > 0$ | $2 > 0$ | ✓ |
| $x = -4$ | $-2 < 0$ | $-8 < 0$ | ✕ (negatifin logaritması yok) |

**Sağlama:** $\log_2 8 + \log_2 2 = 3 + 1 = 4$. ✓

**Sahte çözüm nereden geldi?** Birinci adımda iki logaritmayı birleştirdik. $x = -4$ için $(x+2)(x-4) = (-2)(-8) = 16$ pozitif; birleşik hâl tanımlı görünüyor. Ama orijinal denklemdeki $\log_2(-2)$ ve $\log_2(-8)$ tanımsız. Birleştirmek şartı gizledi, kontrol onu geri getirdi.

**Cevap: 6**
