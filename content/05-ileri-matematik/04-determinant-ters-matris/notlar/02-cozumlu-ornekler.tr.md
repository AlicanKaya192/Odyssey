Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Determinant ve alan

**Soru:** $A = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$ alanı 3 olan bir üçgene uygulanıyor. Yeni üçgenin alanı kaç?

$$
\det A = 4 \cdot 3 - 1 \cdot 2 = 12 - 2 = 10
$$

Determinant alan çarpanı: her şeklin alanı 10 katına çıkıyor. Yeni alan
$3 \cdot 10 = 30$.

## 2. Sıfırları kullanarak 3 × 3 determinant

**Soru:** $\det \begin{bmatrix} 3 & 0 & 2 \\ 1 & 0 & 4 \\ 2 & 5 & 1 \end{bmatrix}$ kaç?

2. sütunda iki sıfır var; o sütun boyunca açalım. Tek sıfır olmayan
eleman $5$, 3. satır 2. sütunda. İşaret deseninde o konum $-$
($+ - +$ / $- + -$ / $+ - +$ tablosunda 3. satır 2. sütun).

$5$'in satırını ve sütununu silince kalan:

$$
\begin{vmatrix} 3 & 2 \\ 1 & 4 \end{vmatrix} = 12 - 2 = 10
$$

$$
\det = -5 \cdot 10 = -50
$$

İlk satır boyunca açsaydık üç terim hesaplamak gerekirdi; sonuç aynı.

## 3. Ters var mı?

**Soru:** $\begin{bmatrix} 2 & 6 \\ 1 & 3 \end{bmatrix}$'in tersi var mı?

$$
\det = 2 \cdot 3 - 6 \cdot 1 = 0
$$

Yok. Neden olduğu da görülüyor: 2. sütun $(6, 3)$, 1. sütunun $(2, 1)$
3 katı. İki sütun aynı doğruda, düzlem o doğruya eziliyor.

## 4. 2 × 2 ters

**Soru:** $A = \begin{bmatrix} 5 & 2 \\ 2 & 1 \end{bmatrix}$'nin tersi nedir?

Önce determinant: $5 \cdot 1 - 2 \cdot 2 = 1$. Sıfır değil, ters var.

Yer değiştir, işaret çevir, $1$'e böl:

$$
A^{-1} = \frac{1}{1} \begin{bmatrix} 1 & -2 \\ -2 & 5 \end{bmatrix} = \begin{bmatrix} 1 & -2 \\ -2 & 5 \end{bmatrix}
$$

Sağlama:

$$
\begin{bmatrix} 5 & 2 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} 1 & -2 \\ -2 & 5 \end{bmatrix} = \begin{bmatrix} 5 - 4 & -10 + 10 \\ 2 - 2 & -4 + 5 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
$$

Determinant $1$ olunca ters de tam sayılı çıkıyor.

## 5. Tersle sistem çözmek

**Soru:** $5x + 2y = 4$ ve $2x + y = 1$ sistemini çöz.

Matris biçimi $A\mathbf{x} = \mathbf{b}$, $A$ 4. örnekteki matris,
$\mathbf{b} = (4, 1)$. Tersi hazır:

$$
\mathbf{x} = A^{-1}\mathbf{b} = \begin{bmatrix} 1 & -2 \\ -2 & 5 \end{bmatrix} \begin{bmatrix} 4 \\ 1 \end{bmatrix} = \begin{bmatrix} 4 - 2 \\ -8 + 5 \end{bmatrix} = \begin{bmatrix} 2 \\ -3 \end{bmatrix}
$$

Sağlama: $5 \cdot 2 + 2 \cdot (-3) = 4$ ✓, $2 \cdot 2 + (-3) = 1$ ✓.

## 6. Kurallarla determinant

**Soru:** $A$ $3 \times 3$ ve $\det A = 3$. $\det(2A)$, $\det(A^\mathsf{T})$, $\det(A^{-1})$ ve $\det(A^2)$ kaç?

- $\det(2A) = 2^3 \cdot 3 = 24$ (üç boyutun her biri 2 kat)
- $\det(A^\mathsf{T}) = \det A = 3$
- $\det(A^{-1}) = \dfrac{1}{3}$
- $\det(A^2) = \det A \cdot \det A = 9$

Hiçbirinde $A$'nın elemanlarını bilmemiz gerekmedi.

## 7. Art arda dönüşümü geri almak

**Soru:** Bir şekil önce $x$ yönünde 2 katına esnetiliyor ($S$), sonra
$90°$ döndürülüyor ($R$). Bunu geri alan dönüşüm nedir?

Toplam dönüşüm $RS$. Tersi $(RS)^{-1} = S^{-1}R^{-1}$: **önce** $R$'yi
geri al ($-90°$ döndür), **sonra** $S$'yi geri al ($x$'i yarıya indir).

$$
R^{-1} = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}
\qquad
S^{-1} = \begin{bmatrix} 0.5 & 0 \\ 0 & 1 \end{bmatrix}
$$

$$
S^{-1}R^{-1} = \begin{bmatrix} 0.5 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 0.5 \\ -1 & 0 \end{bmatrix}
$$

Sağlama: $RS = \begin{bmatrix} 0 & -1 \\ 2 & 0 \end{bmatrix}$ ve
$\begin{bmatrix} 0 & 0.5 \\ -1 & 0 \end{bmatrix} \begin{bmatrix} 0 & -1 \\ 2 & 0 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$. ✓
