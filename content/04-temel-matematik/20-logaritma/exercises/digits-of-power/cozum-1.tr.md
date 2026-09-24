**Ne soruluyor?** $3^{40}$ çok büyük bir sayı. Onu hesaplamadan kaç basamaklı olduğunu bulacağız.

**Fikir:** Basamak sayısı, sayının 10'un hangi iki kuvveti arasında durduğuna bağlı:

- $10^1 = 10$ ile $10^2 = 100$ arasındaki sayılar 2 basamaklı.
- $10^2 = 100$ ile $10^3 = 1000$ arasındakiler 3 basamaklı.

Genel olarak $10^k \le N < 10^{k+1}$ ise $N$, $k + 1$ basamaklı. Bir sayının 10'un hangi kuvvetleri arasında olduğunu da $\log_{10}$ söylüyor.

**Adım 1 — Logaritmayı kuvvet kuralıyla hesapla.** Kuvvet kuralı: $\log_b x^n = n \cdot \log_b x$ (üs öne iner).

$$
\begin{aligned}
\log_{10} 3^{40} &= 40 \cdot \log_{10} 3 \\
&\approx 40 \cdot 0.4771 \\
&= 19.084
\end{aligned}
$$

**Adım 2 — Bu sayının anlamı.** $\log_{10} 3^{40} \approx 19.084$ demek $3^{40} \approx 10^{19.084}$ demek. $19.084$, 19 ile 20 arasında olduğu için:

$$
10^{19} \le 3^{40} < 10^{20}
$$

**Adım 3 — Basamak sayısını oku.** $10^{19}$ bir ve arkasından 19 sıfır, yani **20 basamaklı en küçük sayı**. $10^{20}$ ise 21 basamaklı en küçük sayı. $3^{40}$ ikisinin arasında olduğu için 20 basamaklı.

Formül olarak: logaritmanın tam kısmı artı 1.

$$
\lfloor 19.084 \rfloor + 1 = 19 + 1 = 20
$$

**Sağlama:** Gerçekten de $3^{40} = 12\,157\,665\,459\,056\,928\,801$; saydığında 20 basamak.

**Dikkat:** En sık cevap 19. Logaritmanın tam kısmı basamak sayısının **bir eksiği**; $+1$ unutulmamalı. ($10 = 10^1$ iki basamaklı, logaritması 1.)

**Cevap:** 20.
