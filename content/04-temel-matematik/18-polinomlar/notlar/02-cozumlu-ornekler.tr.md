Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Derece ve baş katsayı

**Soru:** $5 + 3x - x^4 + 2x^2$ polinomunun derecesi, baş katsayısı ve
sabit terimi nedir?

Standart biçime diz: $-x^4 + 2x^2 + 3x + 5$. Derece $4$, baş katsayı $-1$,
sabit terim $5$. Baş katsayı ilk yazılan terimin değil, en büyük kuvvetin
katsayısı.

## 2. Değer hesaplamak

**Soru:** $P(x) = x^3 - 3x + 1$ için $P(-2)$ kaçtır?

$(-2)^3 = -8$ ve $-3 \cdot (-2) = 6$: $P(-2) = -8 + 6 + 1 = -1$. Negatif
sayıyı parantez içinde koymak işaret hatasını önler.

## 3. Çıkarma

**Soru:** $(4x^3 - x + 2) - (x^3 + 2x^2 - 3x + 5)$ nedir?

İkinci parantezin her işareti değişir: $4x^3 - x + 2 - x^3 - 2x^2 + 3x - 5$.
Benzer terimler: $3x^3 - 2x^2 + 2x - 3$.

## 4. Çarpma

**Soru:** $(x + 3)(x^2 - 2x + 4)$ nedir?

$$
\begin{aligned}
&x^3 - 2x^2 + 4x + 3x^2 - 6x + 12 \\
&= x^3 + x^2 - 2x + 12
\end{aligned}
$$

Sınama: $x = 1$ için sol taraf $4 \cdot 3 = 12$, sağ taraf
$1 + 1 - 2 + 12 = 12$ ✓.

## 5. Sentetik bölme

**Soru:** $(x^3 - 8) \div (x - 2)$ işleminin bölümü ve kalanı nedir?

Eksik terimlere yer aç: katsayılar $1, 0, 0, -8$, $a = 2$.

| | $1$ | $0$ | $0$ | $-8$ |
|---|---|---|---|---|
| $a = 2$ | | $2$ | $4$ | $8$ |
| sonuç | $1$ | $2$ | $4$ | $0$ |

Bölüm $x^2 + 2x + 4$, kalan $0$: $x^3 - 8 = (x - 2)(x^2 + 2x + 4)$. Bu, küp
farkı özdeşliği.

## 6. Kalan teoremi

**Soru:** $P(x) = x^4 - 3x^2 + 5$ polinomunun $(x + 1)$ ile bölümünden
kalan kaçtır?

$(x + 1) = (x - (-1))$, yani $a = -1$. $P(-1) = 1 - 3 + 5 = 3$. Bölme
yapmaya gerek yok.

## 7. Bilinmeyen katsayı

**Soru:** $x^3 + ax - 6$ polinomu $(x - 2)$ ile tam bölünüyorsa $a$ kaçtır?

Tam bölünmek kalanın $0$ olması demek, yani $P(2) = 0$:
$8 + 2a - 6 = 0$, buradan $a = -1$.

## 8. Kökleri bulmak

**Soru:** $x^3 - 7x + 6$ polinomunu çarpanlarına ayır.

Adaylar $6$'nın bölenleri. $P(1) = 1 - 7 + 6 = 0$, yani $(x - 1)$ çarpan.
Sentetik bölme ($1, 0, -7, 6$ ve $a = 1$) bölümü $x^2 + x - 6$ verir.
$x^2 + x - 6 = (x + 3)(x - 2)$:

$$
x^3 - 7x + 6 = (x - 1)(x + 3)(x - 2)
$$

Kökler $-3$, $1$, $2$.

## 9. Uç davranışı

**Soru:** $-2x^5 + x$ polinomunun grafiğinin uçları nereye gider?

Derece $5$ (tek), baş katsayı $-2$ (negatif): sol uç yukarı, sağ uç aşağı.
Tek dereceli olduğu için en az bir gerçek kökü var; burada $x = 0$ bir kök.
