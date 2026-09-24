**Ne soruluyor?** Bir veri setinin eğitim, doğrulama ve test diye üçe bölünmesi; testin büyüklüğü ve oranı.

**Fikir:** Adım adım kaç örnek kaldığını bul. "Geri kalanın $\frac{1}{3}$'ü" bütünün değil, eğitimden arta kalanın parçası.

**Adım 1 — Eğitim.**

$$
\frac{7}{10} \cdot 1\,200 = 840
$$

Geriye $1\,200 - 840 = 360$ örnek kalıyor.

**Adım 2 — Doğrulama.**

$$
\frac{1}{3} \cdot 360 = 120
$$

**Adım 3 — Test.** $360 - 120 = 240$ örnek.

**Adım 4 — Oran.**

$$
\frac{240}{1\,200} = \frac{1}{5}
$$

($240$'ı ve $1\,200$'ü $240$'a böldük.)

**Sağlama:** $840 + 120 + 240 = 1\,200$ ✓.

**Sonucu yorumla:** Bölünme yaklaşık %70 eğitim, %10 doğrulama, %20 test; makine öğrenmesinde sık kullanılan bir oran.

**Cevap:** $240$ örnek; verinin $\dfrac{1}{5}$'i.
