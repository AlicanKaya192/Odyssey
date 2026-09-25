**Fikir:** $n$ örnekli, sınıf sayıları $n_k$ olan bir düğümde $H = \log_2 n - \frac{1}{n}\sum n_k\log_2 n_k$. Bölme sayılarla doğrudan hesaplanır.

**Adım 1 — Sol.** $\log_2 6 - \frac{5\log_2 5 + 1 \cdot 0}{6} \approx 2{,}585 - \frac{11{,}610}{6} \approx 2{,}585 - 1{,}935 = 0{,}650$.

**Adım 2 — Sağ ve ortalama.** $\log_2 10 - \frac{3\log_2 3 + 7\log_2 7}{10} \approx 3{,}322 - \frac{4{,}755 + 19{,}651}{10} \approx 3{,}322 - 2{,}441 = 0{,}881$. Ağırlıklı ortalama $\frac{6 \cdot 0{,}650 + 10 \cdot 0{,}881}{16} \approx 0{,}795$.

**Adım 3 — Kazanç.** $1 - 0{,}795 \approx 0{,}205$.

**Neden aynı sonuç?** $-\sum\frac{n_k}{n}\log_2\frac{n_k}{n} = -\sum\frac{n_k}{n}(\log_2 n_k - \log_2 n)$; açınca $\log_2 n - \frac{1}{n}\sum n_k\log_2 n_k$ çıkar. Karar ağacı kütüphaneleri sayılarla bu biçimde çalışır.

**Cevap:** $0{,}650$; $0{,}795$ ve $0{,}205$.
