Ondalıklı sayılarla (float) çalışırken karşına çıkacak beş tuzak, hepsi bu
bilgisayarda ölçüldü:

```python
import math

print(math.isclose(1e-10, 0), math.isclose(1e-10, 0, abs_tol=1e-9))
print(1e16 + 1 == 1e16, 10 ** 16 + 1 == 10 ** 16)
print(7 / 2, 7 // 2, -7 // 2, 7 % 3, -7 % 3)
print(0.1 * 3, float("inf") - float("inf"))
```

```text
False True
True False
3.5 3 -4 1 2
0.30000000000000004 nan
```

1. **Sıfıra yakın karşılaştırma.** `isclose` varsayılan olarak **göreli**
   tolerans kullanır (sayının büyüklüğüne oranla); sıfırla karşılaştırırken
   göreli tolerans sıfırdır ve `1e-10` "sıfıra yakın" sayılmaz. Sıfıra yakınlık
   için `abs_tol` verilir.
2. **Büyük ondalıklarda hassasiyet biter.** `1e16 + 1` yine `1e16`: float
   yaklaşık 15–16 basamak tutar. Tam sayılar (`int`) ise sınırsızdır;
   `10 ** 16 + 1` doğru hesaplanır. Kesinlik gerekiyorsa tam sayıyla çalış.
3. **Bölme türleri.** `/` her zaman float verir (3,5). `//` aşağı yuvarlar,
   sıfıra doğru değil: `-7 // 2` **−4**. `%` da buna uyar: `-7 % 3` **2**.
4. **Gösterilen sayı saklanan sayı değildir.** `0.1 * 3` ekrana
   `0.30000000000000004` olarak çıkar; tutarları yazdırırken `round` ya da
   biçimlendirme (`f"{x:.2f}"`) kullan, hesapta değil.
5. **`inf - inf` bir sayı değildir** (`nan`). `nan` hesaplara sessizce yayılır;
   bir sonuç beklenmedik `nan` çıkarsa geriye doğru `math.isnan` ile ara.

Kesin ondalık (para) için `decimal`, kesir için `fractions` modülleri İleri
Python modülünde.
