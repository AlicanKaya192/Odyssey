**Ne soruluyor?** Modelin tipik hata büyüklüğünü ölçen iki sayı: MSE ve RMSE.

**Fikir:** Hataları doğrudan ortalamak işe yaramaz; pozitif ve negatifler birbirini götürür ($3 - 1 + 2 - 2 = 2$). Kare almak işaretten kurtarır, ortalama tek sayıya indirir, karekök de birimi (hatanın kendi birimini) geri getirir. Adı da bu sırayı söylüyor: **R**oot **M**ean **S**quared **E**rror.

**Adım 1 — Kareler.**

$$
3^2 = 9, \quad (-1)^2 = 1, \quad 2^2 = 4, \quad (-2)^2 = 4
$$

**Adım 2 — Ortalama (MSE).**

$$
\frac{9 + 1 + 4 + 4}{4} = \frac{18}{4} = 4{,}5
$$

**Adım 3 — Karekök (RMSE).** $2{,}1^2 = 4{,}41$ ve $2{,}2^2 = 4{,}84$: kök $2{,}1$ ile $2{,}2$ arasında, $2{,}1$'e yakın. $2{,}12^2 = 4{,}494$ ve $2{,}13^2 = 4{,}537$:

$$
\sqrt{4{,}5} \approx 2{,}12
$$

**Sonucu yorumla:** Hataların büyüklükleri $1$ ile $3$ arasında; RMSE $2{,}12$ bunların "tipik" değeri. Mutlak hataların ortalaması ($\frac{3 + 1 + 2 + 2}{4} = 2$) biraz daha küçük; RMSE büyük hatalara (burada $3$) daha çok ağırlık veriyor.

**Dikkat:** Kök alırken sırayı karıştırıp önce kök sonra ortalama almak ($\frac{3 + 1 + 2 + 2}{4}$) RMSE değil, mutlak hata ortalaması verir.

**Cevap:** MSE $4{,}5$; RMSE $\approx 2{,}12$.
