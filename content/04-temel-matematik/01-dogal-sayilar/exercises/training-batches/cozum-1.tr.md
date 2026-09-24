**Ne soruluyor?** Bir veri setinin yığınlara nasıl bölündüğü ve eğitimin kaç adım süreceği.

**Fikir:** $25\,000$'i $64$'e kalanlı bölersek bölüm tam yığın sayısını, kalan son yığındaki örnek sayısını verir: $25\,000 = 64 \cdot q + r$.

**Adım 1 — Kaba tahmin.** $64 \approx 60$ ve $25\,000 \div 60 \approx 417$; $64$ biraz büyük olduğu için bölüm biraz daha küçük, $400$ civarı.

**Adım 2 — $64 \cdot 400$.** $25\,600$: bu $25\,000$'den büyük, $400$ fazla. Fark $600$; $600 \div 64 \approx 9.4$, yani yaklaşık $10$ yığın eksiltmemiz gerekiyor.

**Adım 3 — $64 \cdot 390$.** $25\,600 - 640 = 24\,960$. Kalan:

$$
25\,000 - 24\,960 = 40
$$

$40 < 64$: bir yığın daha sığmaz.

$$
25\,000 = 64 \cdot 390 + 40
$$

**Adım 4 — Tam yığın ve son yığın.** $390$ tam yığın, son yığında $40$ örnek.

**Adım 5 — Adımlar.** Bir tur $390 + 1 = 391$ adım. Dört tur:

$$
4 \cdot 391 = 1\,564
$$

**Dikkat:** Son eksik yığını unutup $4 \cdot 390 = 1\,560$ yazmak en sık hata; o $40$ örnek de her turda işleniyor.

**Cevap:** $390$ tam yığın; son yığında $40$ örnek; $4$ turda $1\,564$ adım.
