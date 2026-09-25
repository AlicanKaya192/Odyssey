**Fikir:** $-\ln p_2 = -z_2 + \ln\sum_j e^{z_j}$. Olasılıkları tek tek bölmeden kaybı doğrudan yazabiliriz.

**Adım 1 — $p_1$.** $\frac{e^{2}}{11{,}212} \approx 0{,}659$.

**Adım 2 — Kayıp.** $\ln 11{,}212 \approx 2{,}417$; kayıp $-1 + 2{,}417 = 1{,}417$.

**Adım 3 — Türev.** $\frac{\partial}{\partial z_2}\left[-z_2 + \ln\sum_j e^{z_j}\right] = -1 + \frac{e^{z_2}}{\sum_j e^{z_j}} = -1 + p_2 \approx -0{,}758$.

**Neden aynı sonuç?** $\ln\frac{e^{z_2}}{\sum e^{z_j}} = z_2 - \ln\sum e^{z_j}$; log-toplam-üsün türevi de softmax'ın kendisi. Kütüphaneler kaybı bu biçimde hesaplar, çünkü büyük skorlarda $e^{z}$ taşmadan hesaplanabilir.

**Cevap:** $0{,}659$; $1{,}417$ ve $-0{,}758$.
