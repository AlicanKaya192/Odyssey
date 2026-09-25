Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Formüller

| Ne | Formül |
|---|---|
| kovaryans | $\operatorname{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - E[X]E[Y]$ |
| örneklem kovaryansı | $s_{xy} = \frac{1}{n - 1}\sum (x_i - \bar{x})(y_i - \bar{y})$ |
| korelasyon | $r = \frac{s_{xy}}{s_x s_y}$, $\ -1 \leq r \leq 1$ |
| korelasyondan kovaryans | $\operatorname{Cov} = r \, \sigma_X \sigma_Y$ |
| toplamın varyansı | $\operatorname{Var}(X \pm Y) = \operatorname{Var}X + \operatorname{Var}Y \pm 2\operatorname{Cov}(X, Y)$ |
| doğrusal dönüşüm | $\operatorname{Cov}(aX + b, cY + d) = ac\operatorname{Cov}(X, Y)$ |
| kovaryans matrisi | $\Sigma = \frac{1}{n - 1} X^\mathsf{T} X$ (merkezlenmiş $X$) |

## r'yi okumak

| $r$ | Anlamı |
|---|---|
| $1$ ya da $-1$ | noktalar tam bir doğru üzerinde |
| $0{,}7$'den büyük (mutlak) | güçlü doğrusal ilişki |
| $0{,}3$–$0{,}7$ | orta |
| $0{,}3$'ten küçük | zayıf |
| $0$ | doğrusal ilişki yok (başka ilişki olabilir) |

## Kovaryans matrisi

- Köşegen: varyanslar; köşegen dışı: kovaryanslar.
- Simetrik ve pozitif yarı tanımlı.
- Korelasyon matrisinin köşegeni $1$.

## Pratik ipuçları

- Önce saçılım grafiğine bak; sonra $r$'yi hesapla.
- Kovaryansın işaretine güven, büyüklüğüne değil.
- Bağımsızlık kovaryansı sıfırlar; sıfır kovaryans bağımsızlık demek
  değildir.
- Korelasyon nedensellik değildir; gizli değişken ara.
- Aykırı değer varsa Spearman (sıra) korelasyonunu dene.
