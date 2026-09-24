Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Köşegen matris

**Soru:** $\begin{bmatrix} 3 & 0 \\ 0 & -2 \end{bmatrix}$'nin tekil değerleri nedir?

Köşegen bir matris zaten eksenler boyunca esnetiyor: $x$'i 3 katına,
$y$'yi $-2$ katına (2 katına ve ters yöne). Tekil değerler negatif
olamaz; işaret bir yansıma olarak $U$'ya gider. Tekil değerler $3$ ve $2$.

$A^\mathsf{T}A = \begin{bmatrix} 9 & 0 \\ 0 & 4 \end{bmatrix}$ ile de: özdeğerler
$9, 4$, karekökleri $3, 2$ ✓.

## 2. Tam bir SVD

**Soru:** $A = \begin{bmatrix} 2 & 2 \\ -1 & 1 \end{bmatrix}$'nin SVD'sini bul.

$$
A^\mathsf{T}A = \begin{bmatrix} 2 & -1 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} 2 & 2 \\ -1 & 1 \end{bmatrix} = \begin{bmatrix} 5 & 3 \\ 3 & 5 \end{bmatrix}
$$

İz $10$, determinant $16$: özdeğerler $8$ ve $2$. Tekil değerler
$\sigma_1 = 2\sqrt{2} \approx 2.83$, $\sigma_2 = \sqrt{2} \approx 1.41$.

Özvektörler: $\lambda = 8$ için $y = x$, $\lambda = 2$ için $y = -x$.

$$
\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(1, 1)
\qquad
\mathbf{v}_2 = \tfrac{1}{\sqrt{2}}(1, -1)
$$

$A\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(4, 0)$, $\sigma_1$'e bölünce $\mathbf{u}_1 = (1, 0)$.
$A\mathbf{v}_2 = \tfrac{1}{\sqrt{2}}(0, -2)$, $\sigma_2$'ye bölünce $\mathbf{u}_2 = (0, -1)$.

Sağlama: $\sigma_1\sigma_2 = 2\sqrt{2} \cdot \sqrt{2} = 4 = |\det A| = |2 + 2|$ ✓.

## 3. Dikdörtgen bir matris

**Soru:** $A = \begin{bmatrix} 1 & 1 \\ 1 & 1 \\ 0 & 0 \end{bmatrix}$'nin tekil değerleri ve rankı nedir?

$A$ $3 \times 2$; $A^\mathsf{T}A$ $2 \times 2$:

$$
A^\mathsf{T}A = \begin{bmatrix} 2 & 2 \\ 2 & 2 \end{bmatrix}
$$

Özdeğerler $4$ ve $0$ (iz 4, determinant 0). Tekil değerler $2$ ve $0$:
rank $1$. Gerçekten de iki sütun aynı.

## 4. Rank-1 matris

**Soru:** $A = \begin{bmatrix} 2 & 4 \\ 1 & 2 \end{bmatrix}$'nin SVD'si nedir?

Her satır $(1, 2)$'nin katı: $A = \begin{bmatrix} 2 \\ 1 \end{bmatrix} \begin{bmatrix} 1 & 2 \end{bmatrix}$.
Tek bir katman var:

$$
\sigma_1 = \|(2, 1)\| \cdot \|(1, 2)\| = \sqrt{5} \cdot \sqrt{5} = 5
$$

$\mathbf{u}_1 = \tfrac{1}{\sqrt{5}}(2, 1)$, $\mathbf{v}_1 = \tfrac{1}{\sqrt{5}}(1, 2)$, $\sigma_2 = 0$.

Sağlama: elemanların kareleri toplamı $4 + 16 + 1 + 4 = 25 = \sigma_1^2$ ✓.

## 5. Enerji payı

**Soru:** Bir matrisin tekil değerleri $20, 10, 5, 2, 1$. Rankı 2 ve rankı 3
olan yaklaşımlar enerjinin ne kadarını korur?

Kareler: $400, 100, 25, 4, 1$; toplam $530$.

- Rank 2: $\dfrac{400 + 100}{530} = \dfrac{500}{530} \approx 0.943$, yani %94.3.
- Rank 3: $\dfrac{525}{530} \approx 0.991$, yani %99.1.

Rank 3 yaklaşımının hatası $\sqrt{4 + 1} = \sqrt{5} \approx 2.24$.

## 6. Koşul sayısı

**Soru:** Kare bir matrisin en büyük tekil değeri $100$, en küçüğü $0.01$. Koşul sayısı nedir?

$$
\frac{\sigma_1}{\sigma_n} = \frac{100}{0.01} = 10\,000
$$

Matris tersinir ama "neredeyse tekil": çözümde girdideki küçük bir hata
$10\,000$ katına kadar büyüyebilir.

## 7. Saklama

**Soru:** $256 \times 256$ gri tonlu bir görüntü için rankı 20 olan yaklaşım kaç sayı saklar?

$$
20 \cdot (256 + 256 + 1) = 20 \cdot 513 = 10\,260
$$

Orijinal $256 \cdot 256 = 65\,536$ sayı; yaklaşım yaklaşık %15.7'si.
