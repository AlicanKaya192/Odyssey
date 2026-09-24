**Ne soruluyor?** Bir $3 \times 3$ determinant ve matris 2 ile çarpılınca determinantın ne olduğu.

**Fikir:** İlk satır boyunca açılım: her ilk satır elemanı, kendi satırı ve sütunu silinince kalan $2 \times 2$ determinantla çarpılır; işaretler $+, -, +$.

**Adım 1 — $a_{11} = 2$.** 1. satırı ve 1. sütunu sil; kalan $\begin{bmatrix} 3 & 2 \\ 1 & 2 \end{bmatrix}$:

$$
2 \cdot (3 \cdot 2 - 2 \cdot 1) = 2 \cdot 4 = 8
$$

**Adım 2 — $a_{12} = 0$.** Sıfır çarpı her şey sıfır; bu terimi hesaplamaya gerek yok.

**Adım 3 — $a_{13} = 1$.** 1. satırı ve 3. sütunu sil; kalan $\begin{bmatrix} 1 & 3 \\ 1 & 1 \end{bmatrix}$:

$$
1 \cdot (1 \cdot 1 - 3 \cdot 1) = -2
$$

**Adım 4 — İşaretlerle topla.**

$$
\det A = 8 - 0 + (-2) = 6
$$

**Adım 5 — $\det(2A)$.** $2A$'da üç satırın her biri 2 ile çarpılıyor. Bir satırı 2 ile çarpmak determinantı 2 ile çarpar; üç satır için $2 \cdot 2 \cdot 2 = 2^3 = 8$:

$$
\det(2A) = 2^3 \cdot \det A = 8 \cdot 6 = 48
$$

**Dikkat:** $\det(2A) = 2 \cdot 6 = 12$ en sık yapılan hata. Geometrik olarak: küpün üç kenarı da 2 katına çıkınca hacim 8 katına çıkar.

**Cevap:** $\det A = 6$, $\det(2A) = 48$.
