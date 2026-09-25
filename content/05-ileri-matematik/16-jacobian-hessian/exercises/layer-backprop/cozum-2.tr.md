**Fikir:** Katman küçük; kaybı doğrudan $x_1$, $x_2$ ve $W_{12}$ cinsinden yazıp kısmi türev al. ($\mathbf{z}$'ler pozitif kaldığı sürece ReLU etkisiz.)

**Adım 1 — Kayıp.** $z_1 = W_{11}x_1 + W_{12}x_2$, $z_2 = 3x_1 - x_2$:

$$
L = \tfrac{1}{2}(z_1 - 1)^2 + \tfrac{1}{2}(z_2 - 1)^2
$$

**Adım 2 — $x$'lere göre.** $\frac{\partial L}{\partial x_1} = (z_1 - 1) \cdot 1 + (z_2 - 1) \cdot 3 = 2 + 3 = 5$. $\frac{\partial L}{\partial x_2} = (z_1 - 1) \cdot 2 + (z_2 - 1)(-1) = 4 - 1 = 3$.

**Adım 3 — $W_{12}$'ye göre.** Yalnızca $z_1$ içinde, katsayısı $x_2$: $(z_1 - 1) \cdot x_2 = 2$.

**Neden aynı sonuç?** Her kısmi türev bütün yolların toplamı: $x_1$, $L$'ye hem $z_1$ (katsayı $1$) hem $z_2$ (katsayı $3$) üzerinden bağlı. $W^\mathsf{T}$ ile çarpmak bu toplamların hepsini tek bir matris işleminde yapıyor: $W^\mathsf{T}$'nin $j$'nci satırı, $x_j$'nin bütün $z$'lere giden katsayıları.

**Cevap:** $5$, $3$, $2$.
