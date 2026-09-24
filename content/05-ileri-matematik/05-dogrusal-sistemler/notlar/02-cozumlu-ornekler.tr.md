Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. İki bilinmeyenli sistem

**Soru:** $2x - y = 3$ ve $x + 4y = -3$ sistemini elemeyle çöz.

Artırılmış matris; pivotu $1$ olan denklemi üste almak için satırların
yerini değiştiriyoruz:

$$
\left[\begin{array}{cc|c} 2 & -1 & 3 \\ 1 & 4 & -3 \end{array}\right]
\xrightarrow{R_1 \leftrightarrow R_2}
\left[\begin{array}{cc|c} 1 & 4 & -3 \\ 2 & -1 & 3 \end{array}\right]
$$

$R_2 \to R_2 - 2R_1$:

$$
\left[\begin{array}{cc|c} 1 & 4 & -3 \\ 0 & -9 & 9 \end{array}\right]
$$

Geri yerine koyma: $-9y = 9 \Rightarrow y = -1$; $x + 4 \cdot (-1) = -3
\Rightarrow x = 1$.

Sağlama: $2 \cdot 1 - (-1) = 3$ ✓, $1 + 4 \cdot (-1) = -3$ ✓.

## 2. Sıfır pivot

**Soru:** $y + z = 3$, $x + y + z = 4$, $2x + y + 3z = 9$ sistemini çöz.

İlk satırın ilk elemanı $0$: pivot olamaz. 1. ve 2. satırın yerini
değiştir:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & 1 & 1 & 3 \\ 2 & 1 & 3 & 9 \end{array}\right]
$$

$R_3 \to R_3 - 2R_1$, sonra $R_3 \to R_3 + R_2$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & 1 & 1 & 3 \\ 0 & -1 & 1 & 1 \end{array}\right]
\;\to\;
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & 1 & 1 & 3 \\ 0 & 0 & 2 & 4 \end{array}\right]
$$

$2z = 4 \Rightarrow z = 2$; $y + 2 = 3 \Rightarrow y = 1$;
$x + 1 + 2 = 4 \Rightarrow x = 1$.

## 3. Çözümü olmayan sistem

**Soru:** $x + 2y = 4$ ve $3x + 6y = 10$ sisteminin çözümü var mı?

$R_2 \to R_2 - 3R_1$:

$$
\left[\begin{array}{cc|c} 1 & 2 & 4 \\ 0 & 0 & -2 \end{array}\right]
$$

Son satır $0 = -2$ diyor: imkânsız. **Çözüm yok.** Geometrik olarak iki
doğru paralel: ikinci denklemin sol tarafı birincinin 3 katı, ama sağ
taraf ($10$) $3 \cdot 4 = 12$ değil.

## 4. Sonsuz çözüm

**Soru:** $x + y - z = 1$ ve $2x + 3y + z = 6$ sisteminin bütün çözümlerini bul.

İki denklem, üç bilinmeyen. $R_2 \to R_2 - 2R_1$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & -1 & 1 \\ 0 & 1 & 3 & 4 \end{array}\right]
$$

3. sütunda pivot yok: $z$ serbest, $z = t$.

$$
\begin{aligned}
y &= 4 - 3t \\
x &= 1 - y + z = 1 - (4 - 3t) + t = -3 + 4t
\end{aligned}
$$

Çözüm kümesi $(-3 + 4t,\ 4 - 3t,\ t)$. Sağlama için $t = 0$:
$(-3, 4, 0)$; $-3 + 4 - 0 = 1$ ✓, $-6 + 12 + 0 = 6$ ✓.

## 5. Gauss–Jordan ile ters

**Soru:** $A = \begin{bmatrix} 2 & 3 \\ 1 & 2 \end{bmatrix}$'nin tersini
$[A \mid I]$ yöntemiyle bul.

$$
\left[\begin{array}{cc|cc} 2 & 3 & 1 & 0 \\ 1 & 2 & 0 & 1 \end{array}\right]
\xrightarrow{R_1 \leftrightarrow R_2}
\left[\begin{array}{cc|cc} 1 & 2 & 0 & 1 \\ 2 & 3 & 1 & 0 \end{array}\right]
$$

$$
\xrightarrow{R_2 - 2R_1}
\left[\begin{array}{cc|cc} 1 & 2 & 0 & 1 \\ 0 & -1 & 1 & -2 \end{array}\right]
\xrightarrow{-R_2}
\left[\begin{array}{cc|cc} 1 & 2 & 0 & 1 \\ 0 & 1 & -1 & 2 \end{array}\right]
$$

$$
\xrightarrow{R_1 - 2R_2}
\left[\begin{array}{cc|cc} 1 & 0 & 2 & -3 \\ 0 & 1 & -1 & 2 \end{array}\right]
$$

$A^{-1} = \begin{bmatrix} 2 & -3 \\ -1 & 2 \end{bmatrix}$. Formülle sağlama:
$\det A = 4 - 3 = 1$, yer değiştir ve işaret çevir: aynı matris. ✓

## 6. Elemeyle determinant

**Soru:** $\det \begin{bmatrix} 2 & 1 & 3 \\ 4 & 5 & 7 \\ -2 & 2 & 1 \end{bmatrix}$ kaç?

Yalnızca ekleme işlemleriyle basamak biçimine getirelim.
$R_2 \to R_2 - 2R_1$, $R_3 \to R_3 + R_1$:

$$
\begin{bmatrix} 2 & 1 & 3 \\ 0 & 3 & 1 \\ 0 & 3 & 4 \end{bmatrix}
$$

$R_3 \to R_3 - R_2$:

$$
\begin{bmatrix} 2 & 1 & 3 \\ 0 & 3 & 1 \\ 0 & 0 & 3 \end{bmatrix}
$$

Yer değiştirme yok; determinant pivotların çarpımı: $2 \cdot 3 \cdot 3 = 18$.
