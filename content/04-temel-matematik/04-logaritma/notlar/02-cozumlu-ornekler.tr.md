Derste gördüğün yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Aynı tabana çevirerek logaritma

**Soru:** $\log_4 8$ kaçtır?

8, 4'ün tam bir kuvveti değil. Ama ikisi de 2'nin kuvveti: $4 = 2^2$, $8 = 2^3$.

$\log_4 8 = y$ ise $4^y = 8$:

$$
(2^2)^y = 2^3
\quad\Rightarrow\quad
2^{2y} = 2^3
\quad\Rightarrow\quad
2y = 3
\quad\Rightarrow\quad
y = \frac{3}{2}
$$

**Sağlama:** $4^{3/2} = (\sqrt{4})^3 = 2^3 = 8$. ✓

Aynı yöntemle $\log_9 3 = \frac{1}{2}$ ($9^{1/2} = 3$) ve
$\log_8 2 = \frac{1}{3}$ ($8^{1/3} = 2$).

## 2. Kuralları birlikte kullanarak sadeleştirme

**Soru:** $2 \log_3 6 - \log_3 4$ kaçtır?

**1. Katsayıyı kuvvet kuralıyla içeri al:**

$$
2 \log_3 6 = \log_3 6^2 = \log_3 36
$$

**2. Farkı bölüm kuralıyla birleştir:**

$$
\log_3 36 - \log_3 4 = \log_3 \frac{36}{4} = \log_3 9
$$

**3.** $3^2 = 9$, öyleyse cevap $2$.

Sıra önemli: **önce katsayıları içeri al, sonra birleştir.** Sık yapılan hata
2'yi ifadenin tamamına uygulamak: $2 (\log_3 6 - \log_3 4) = 2 \log_3 1.5 \approx 0.74$
bambaşka bir sayı. İfadede 2 yalnızca ilk terimin katsayısı.

## 3. Tabanlar aynıysa logaritmaya gerek yok

**Soru:** $2^{3x - 1} = 32$

32'yi 2'nin kuvveti olarak yaz: $32 = 2^5$.

$$
2^{3x - 1} = 2^5
\quad\Rightarrow\quad
3x - 1 = 5
\quad\Rightarrow\quad
x = 2
$$

Üstel fonksiyon bire bir olduğu için tabanlar eşitse üsler eşit. Logaritma
almak da aynı sonucu verir ama gereksiz iş.

## 4. Katsayılı üstel denklem

**Soru:** $5 \cdot 3^x = 25$

**1. Üslü terimi yalnız bırak:** $3^x = 5$.

5, 3'ün tam kuvveti değil; logaritma gerekiyor.

**2. Logaritma al ve üssü indir:**

$$
x \ln 3 = \ln 5
\quad\Rightarrow\quad
x = \frac{\ln 5}{\ln 3} \approx \frac{1.609}{1.099} \approx 1.465
$$

**Mantık kontrolü:** $3^1 = 3$ ve $3^2 = 9$; 5 bunların arasında, $x$ de 1 ile
2 arasında. ✓

## 5. Büyüme problemi

**Soru:** 200 kişilik bir topluluk her yıl %10 büyüyor. Kaç yılda 1000 kişi
olur?

$$
200 \cdot 1.1^t = 1000
\quad\Rightarrow\quad
1.1^t = 5
\quad\Rightarrow\quad
t = \frac{\ln 5}{\ln 1.1} \approx \frac{1.609}{0.0953} \approx 16.89
$$

Yaklaşık 17 yıl. Büyüme problemlerinin hepsi bu kalıpta:
**başlangıç · (1 + oran)ᵗ = hedef.** Azalan büyüklüklerde oran eksi
işaretli (%20 azalma için $0.8$).

## 6. Logaritmalı denklem ve kontrol

**Soru:** $\log_3 x + \log_3 (x - 8) = 2$

**1. Birleştir:** $\log_3 \big(x(x - 8)\big) = 2$

**2. Tanıma çevir:** $x(x - 8) = 3^2 = 9$

**3. Çöz:** $x^2 - 8x - 9 = 0$, yani $(x - 9)(x + 1) = 0$. Adaylar: $9$ ve $-1$.

**4. Kontrol et:**

- $x = 9$: $\log_3 9 + \log_3 1 = 2 + 0 = 2$. ✓
- $x = -1$: $\log_3 (-1)$ tanımsız. ✕

**Cevap: $x = 9$.**

## 7. Hesap makinesi olmadan tahmin

**Soru:** $\log_{10} 3000$ yaklaşık kaçtır? ($\log_{10} 3 \approx 0.477$)

Sayıyı "bir sayı çarpı 10'un kuvveti" olarak yaz:

$$
\log_{10} 3000 = \log_{10} (3 \cdot 10^3) = \log_{10} 3 + 3 \approx 3.477
$$

Tam kısım (3) basamak sayısının bir eksiği, ondalık kısım (0.477) ise baştaki
rakamlardan geliyor. 3000, 30 000 ve 300 000'in logaritmaları aynı ondalık
kısmı paylaşıyor: $3.477$, $4.477$, $5.477$.
