Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Dik yapan değeri bulmak

**Soru:** $(2, k, 1)$ ile $(3, -1, 4)$ dik olsun. $k$ kaçtır?

Dik iseler nokta çarpımları sıfır:

$$
2 \cdot 3 + k \cdot (-1) + 1 \cdot 4 = 0 \;\Rightarrow\; 10 - k = 0 \;\Rightarrow\; k = 10
$$

Açı ölçmeye gerek kalmadan, tek bir doğrusal denklem.

## 2. Dar açı

**Soru:** $(1, 2)$ ile $(3, 1)$ arasındaki açı kaç derecedir?

$$
\mathbf{a} \cdot \mathbf{b} = 3 + 2 = 5
\qquad
\|\mathbf{a}\| = \sqrt{5}
\qquad
\|\mathbf{b}\| = \sqrt{10}
$$

$$
\cos\theta = \frac{5}{\sqrt{5}\sqrt{10}} = \frac{5}{\sqrt{50}} = \frac{5}{5\sqrt{2}} = \frac{1}{\sqrt{2}}
\quad\Rightarrow\quad \theta = 45°
$$

Kareköklerin çarpımı tek karekök olarak yazılabilir:
$\sqrt{5}\sqrt{10} = \sqrt{50} = 5\sqrt{2}$.

## 3. Geniş açı

**Soru:** $(2, -1)$ ile $(1, 3)$ arasındaki açı $90°$'den büyük mü?

Açıyı hesaplamadan işarete bak:

$$
(2, -1) \cdot (1, 3) = 2 - 3 = -1 < 0
$$

Negatif, öyleyse açı $90°$'den büyük. Tam değeri istersen
$\cos\theta = \frac{-1}{\sqrt{5}\sqrt{10}} \approx -0.141$ ve
$\theta \approx 98.1°$.

## 4. Uzunluk ve açıdan nokta çarpımı

**Soru:** $\|\mathbf{a}\| = 4$, $\|\mathbf{b}\| = 3$ ve aralarındaki açı $60°$ ise $\mathbf{a} \cdot \mathbf{b}$ kaçtır?

$$
\mathbf{a} \cdot \mathbf{b} = 4 \cdot 3 \cdot \cos 60° = 12 \cdot 0.5 = 6
$$

Bileşenleri bilmeden de nokta çarpımı hesaplanabiliyor.

## 5. İzdüşüm

**Soru:** $\mathbf{a} = (4, 3)$ vektörünün $\mathbf{b} = (1, 1)$ doğrultusundaki izdüşümü nedir?

$$
\mathbf{a} \cdot \mathbf{b} = 7 \qquad \mathbf{b} \cdot \mathbf{b} = 2
$$

Vektör izdüşüm:

$$
\frac{7}{2}\,(1, 1) = (3.5,\ 3.5)
$$

Skaler izdüşüm (gölgenin uzunluğu): $\dfrac{7}{\sqrt{2}} \approx 4.95$.
Sağlama: $\|(3.5, 3.5)\| = 3.5\sqrt{2} \approx 4.95$. ✓

## 6. Kosinüs benzerliğiyle öneri

**Soru:** Kullanıcılar dört filme 0–5 arası puan vermiş. A'ya B mi daha benzer, C mi?

| | Film 1 | Film 2 | Film 3 | Film 4 |
|---|---|---|---|---|
| A | 5 | 3 | 0 | 1 |
| B | 4 | 0 | 0 | 1 |
| C | 0 | 1 | 5 | 4 |

$$
\cos(A, B) = \frac{20 + 0 + 0 + 1}{\sqrt{35}\,\sqrt{17}} = \frac{21}{\sqrt{595}} \approx 0.86
$$

$$
\cos(A, C) = \frac{0 + 3 + 0 + 4}{\sqrt{35}\,\sqrt{42}} = \frac{7}{\sqrt{1470}} \approx 0.18
$$

B çok daha benzer. B'nin sevip A'nın henüz izlemediği filmler, A'ya
önerilecek ilk adaylar.

## 7. Üç norm

**Soru:** $(2, -6, 3)$ vektörünün $L_1$, $L_2$ ve $L_\infty$ normları nedir?

$$
L_1 = 2 + 6 + 3 = 11
\qquad
L_2 = \sqrt{4 + 36 + 9} = \sqrt{49} = 7
\qquad
L_\infty = 6
$$

Sıra her zaman aynı: $6 \le 7 \le 11$.
