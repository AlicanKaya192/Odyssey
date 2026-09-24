Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Germenin içinde mi?

**Soru:** $(5, 7)$, $(1, 2)$ ve $(2, 3)$'ün germesinde mi? İçindeyse katsayılar ne?

$c_1(1, 2) + c_2(2, 3) = (5, 7)$:

$$
\begin{aligned}
c_1 + 2c_2 &= 5 \\
2c_1 + 3c_2 &= 7
\end{aligned}
$$

Birinciden $c_1 = 5 - 2c_2$; ikinciye koy: $10 - 4c_2 + 3c_2 = 7$, yani
$c_2 = 3$ ve $c_1 = -1$.

Sağlama: $-1 \cdot (1, 2) + 3 \cdot (2, 3) = (-1 + 6,\ -2 + 9) = (5, 7)$ ✓.

Aslında hesap yapmadan da "evet" diyebilirdik: $(1, 2)$ ve $(2, 3)$ aynı
doğrultuda değil, düzlemin tamamını geriyorlar.

## 2. Üç vektör bağımsız mı?

**Soru:** $(1, 1, 0)$, $(0, 1, 1)$, $(1, 2, 1)$ bağımsız mı?

Vektörleri sütun yap ve ele. $R_2 - R_1$, sonra $R_3 - R_2$:

$$
\begin{bmatrix} 1 & 0 & 1 \\ 1 & 1 & 2 \\ 0 & 1 & 1 \end{bmatrix}
\to
\begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \\ 0 & 1 & 1 \end{bmatrix}
\to
\begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 0 \end{bmatrix}
$$

3. sütunda pivot yok: **bağımlı**. Gerçekten de 3. vektör ilk ikisinin
toplamı: $(1, 1, 0) + (0, 1, 1) = (1, 2, 1)$.

## 3. Bağımlı olmaları için k

**Soru:** $(1, k)$ ve $(k, 4)$ hangi $k$ değerlerinde bağımlıdır?

İki vektör; kare matris kurup determinantı sıfıra eşitle:

$$
\det \begin{bmatrix} 1 & k \\ k & 4 \end{bmatrix} = 4 - k^2 = 0
$$

$k = 2$ ya da $k = -2$. $k = 2$ için $(1, 2)$ ve $(2, 4)$: ikincisi
birincinin 2 katı ✓. $k = -2$ için $(1, -2)$ ve $(-2, 4)$: $-2$ katı ✓.

## 4. Başka bir tabanda koordinat

**Soru:** $\mathbf{b}_1 = (1, 2)$, $\mathbf{b}_2 = (1, -1)$ tabanında
$(4, 5)$'in koordinatları nedir?

$$
\begin{aligned}
c_1 + c_2 &= 4 \\
2c_1 - c_2 &= 5
\end{aligned}
$$

Topla: $3c_1 = 9$, $c_1 = 3$; sonra $c_2 = 1$.

Sağlama: $3(1, 2) + 1(1, -1) = (4, 5)$ ✓. Yeni koordinatlar $(3, 1)$.

## 5. Rank

**Soru:** Aşağıdaki matrisin rankı ve çekirdeğinin boyutu nedir?

$$
A = \begin{bmatrix} 1 & 2 & 0 & 1 \\ 2 & 4 & 1 & 4 \\ 3 & 6 & 1 & 5 \end{bmatrix}
$$

$R_2 - 2R_1$ ve $R_3 - 3R_1$:

$$
\begin{bmatrix} 1 & 2 & 0 & 1 \\ 0 & 0 & 1 & 2 \\ 0 & 0 & 1 & 2 \end{bmatrix}
$$

$R_3 - R_2$ son satırı sıfırlar. Pivotlar 1. ve 3. sütunda: $\operatorname{rank} A = 2$.
Rank–sıfırlıktan çekirdeğin boyutu $4 - 2 = 2$.

## 6. Çekirdeğin tabanı

**Soru:** 5. örnekteki $A$'nın çekirdeğini bul.

Basamak biçimindeki denklemler:

$$
\begin{aligned}
x_1 + 2x_2 + x_4 &= 0 \\
x_3 + 2x_4 &= 0
\end{aligned}
$$

Serbest değişkenler $x_2 = s$, $x_4 = t$. Öteki ikisi:
$x_3 = -2t$, $x_1 = -2s - t$.

$$
\mathbf{x} = s \begin{bmatrix} -2 \\ 1 \\ 0 \\ 0 \end{bmatrix} + t \begin{bmatrix} -1 \\ 0 \\ -2 \\ 1 \end{bmatrix}
$$

Çekirdeğin tabanı bu iki vektör (boyut 2 ✓). Sağlama:
$A(-1, 0, -2, 1) = (-1 + 0 + 0 + 1,\ -2 + 0 - 2 + 4,\ -3 + 0 - 2 + 5) = (0, 0, 0)$ ✓.
