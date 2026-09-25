Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Tek özellik

| Ne | Formül |
|---|---|
| model | $\hat{y} = b + wx$ |
| eğim | $w = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2} = r\frac{s_y}{s_x}$ |
| kesişim | $b = \bar{y} - w\bar{x}$ |
| kesişimsiz model | $w = \frac{\sum x_i y_i}{\sum x_i^2}$ |

## Matris biçimi

| Ne | Formül |
|---|---|
| kayıp | $\text{SSE} = \lVert y - Xw \rVert^2$ |
| gradyan | $-2X^\mathsf{T}(y - Xw)$ |
| normal denklemler | $X^\mathsf{T}Xw = X^\mathsf{T}y$ |
| çözüm | $w = (X^\mathsf{T}X)^{-1}X^\mathsf{T}y$ |
| ridge | $w = (X^\mathsf{T}X + \lambda I)^{-1}X^\mathsf{T}y$ |

$2 \times 2$ ters: $\begin{pmatrix} a & b \\ c & d \end{pmatrix}^{-1} =
\frac{1}{ad - bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$.

## Uyum

| Ne | Formül |
|---|---|
| kalıntı | $e_i = y_i - \hat{y}_i$, $\sum e_i = 0$ |
| SST | $\sum (y_i - \bar{y})^2$ |
| $R^2$ | $1 - \frac{\text{SSE}}{\text{SST}}$ (tek özellikte $r^2$) |
| gürültü varyansı | MLE $\frac{\text{SSE}}{n}$, yansız $\frac{\text{SSE}}{n - d - 1}$ |

## Pratik ipuçları

- $X$'in başına $1$ sütununu eklemeyi unutma.
- Doğru $(\bar{x}, \bar{y})$'den geçer; kontrol için kullan.
- Kalıntılar her sütunla dik: $X^\mathsf{T}e = 0$.
- $X^\mathsf{T}X$'in determinantı sıfıra yakınsa çoklu doğrusallık var;
  ridge dene.
