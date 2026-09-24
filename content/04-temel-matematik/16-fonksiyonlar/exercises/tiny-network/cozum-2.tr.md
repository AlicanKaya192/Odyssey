**Fikir:** ReLU iki durumlu: içi negatifse $0$, değilse kendisi. Ağı iki parçalı tek bir fonksiyon olarak yaz, sonra girdileri koy.

**Adım 1 — Sınır.** $2x - 3 \ge 0 \Leftrightarrow x \ge 1{,}5$.

**Adım 2 — İki parça.**

$$
y = \begin{cases} 3(2x - 3) + 1 = 6x - 8, & x \ge 1{,}5 \\ 3 \cdot 0 + 1 = 1, & x < 1{,}5 \end{cases}
$$

**Adım 3 — Değerler.** $x = 4 \ge 1{,}5$: $y = 24 - 8 = 16$. $x = 1 < 1{,}5$: $y = 1$.

**Neden aynı sonuç?** Katman katman hesap, her girdide bu parçalardan birini seçip uyguluyor. Parçalı yazım bunu bütün girdiler için bir kerede gösteriyor ve ağın ReLU sayesinde nasıl "kırılabildiğini" açıkça ortaya koyuyor.

**Cevap:** $16$ ve $1$.
