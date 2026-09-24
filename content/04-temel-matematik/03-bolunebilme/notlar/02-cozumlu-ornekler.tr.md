Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Bölünebilme kurallarını birlikte kullanmak

**Soru:** $7\,452$ sayısı $2, 3, 4, 6, 9$'dan hangilerine bölünür?

- $2$: son rakam $2$, çift ✓
- $3$ ve $9$: $7 + 4 + 5 + 2 = 18$; $18$ hem $3$'ün hem $9$'un katı ✓ ✓
- $4$: son iki rakam $52 = 4 \cdot 13$ ✓
- $6$: $2$ ve $3$'e bölündüğü için ✓

Beşine de bölünüyor.

## 2. Asallık testi

**Soru:** $91$ asal mı?

$10 \cdot 10 = 100 > 91$ olduğu için $2, 3, 5, 7$'ye bakmak yeter. $2$:
tek. $3$: $9 + 1 = 10$, hayır. $5$: son rakam $1$, hayır. $7$: $7 \cdot
13 = 91$. **Asal değil.**

## 3. Asal çarpanlara ayırma

**Soru:** $504$'ü asal çarpanlarına ayır.

Küçük asallarla sırayla böl:

$$
504 \xrightarrow{\div 2} 252 \xrightarrow{\div 2} 126 \xrightarrow{\div 2} 63 \xrightarrow{\div 3} 21 \xrightarrow{\div 3} 7
$$

$$
504 = 2^3 \cdot 3^2 \cdot 7
$$

## 4. Bölen sayısı

**Soru:** $504$'ün kaç böleni var?

Üsler $3, 2, 1$: $(3 + 1)(2 + 1)(1 + 1) = 24$.

## 5. EBOB ve EKOK asal çarpanlarla

**Soru:** $\text{EBOB}(60, 72)$ ve $\text{EKOK}(60, 72)$ nedir?

$$
60 = 2^2 \cdot 3 \cdot 5, \qquad 72 = 2^3 \cdot 3^2
$$

EBOB: ortak asallar $2$ ve $3$, küçük üsler: $2^2 \cdot 3 = 12$.

EKOK: bütün asallar, büyük üsler: $2^3 \cdot 3^2 \cdot 5 = 360$.

Kontrol: $12 \cdot 360 = 4\,320 = 60 \cdot 72$ ✓.

## 6. Öklid algoritması

**Soru:** $\text{EBOB}(252, 198)$ nedir?

$$
\begin{aligned}
252 &= 198 \cdot 1 + 54 \\
198 &= 54 \cdot 3 + 36 \\
54 &= 36 \cdot 1 + 18 \\
36 &= 18 \cdot 2 + 0
\end{aligned}
$$

EBOB $18$.

## 7. EBOB problemi

**Soru:** $48$ cm ve $80$ cm uzunluğundaki iki çubuk, hiç artık kalmadan
eşit uzunlukta en uzun parçalara kesilecek. Parça kaç cm, toplam kaç
parça?

Parça boyu ikisini de bölmeli ve en büyük olmalı: $\text{EBOB}(48, 80) =
16$ cm. Parça sayısı $48 \div 16 + 80 \div 16 = 3 + 5 = 8$.

## 8. EKOK problemi

**Soru:** Üç lamba $4$, $6$ ve $10$ saniyede bir yanıyor. Birlikte
yandıktan kaç saniye sonra yeniden birlikte yanarlar?

$4 = 2^2$, $6 = 2 \cdot 3$, $10 = 2 \cdot 5$. EKOK $= 2^2 \cdot 3 \cdot 5
= 60$ saniye.
