**Fikir:** Özdeğer hesaplamadan dışbükeyliği göster: ifadeyi dışbükey parçaların toplamı olarak yaz.

**Adım 1 — Düzenle.** $2x^2 + 2xy + y^2 = x^2 + (x^2 + 2xy + y^2) = x^2 + (x + y)^2$.

**Adım 2 — Kurallar.** $x^2$ dışbükey. $(x + y)^2$, dışbükey $u^2$'ye doğrusal $u = x + y$ konmuş hâli: dışbükey. Toplam dışbükey.

**Adım 3 — Sayılar.** Determinant ve özdeğerler için yine Hessian gerekir: $\det H = 4$, özdeğerler $3 \pm \sqrt{5}$, küçüğü $0{,}764$.

**Neden aynı sonuç?** Kareler toplamı ancak $x = 0$ ve $x + y = 0$ iken sıfır; yani yalnızca başlangıçta. Bu, Hessian'ın özdeğerlerinin kesin pozitif olmasının cebirsel karşılığı: $\mathbf{h}^\mathsf{T} H \mathbf{h} = 2\big(h_1^2 + (h_1 + h_2)^2\big) > 0$.

**Cevap:** $4$ ve $0{,}764$.
