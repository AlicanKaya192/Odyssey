Web trafiğinde mevsimsel naifin tek adımlı hatasına bak ve birkaç aykırı
günün MAE ile RMSE'yi ne kadar farklı etkilediğini ölç.

**Yapman gerekenler:**

1. Tek adımlı hatayı hesapla: `error = (visits - visits.shift(7)).dropna()`.
2. MAE'yi, RMSE'yi (bir ondalık) ve RMSE / MAE oranını (iki ondalık) aynı
   satıra yazdır.
3. Mutlak hatası en büyük 6 günü `"%m-%d"` biçiminde, **tarih sırasıyla**
   liste olarak yazdır.
4. Bu 6 günü çıkar ve aynı üç sayıyı yeniden yazdır.
5. 6 günün çıkarılmasıyla MAE ve RMSE yüzde kaç düştü? İkisini tam sayıya
   yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
307.2 728.6 2.37
['03-14', '03-21', '06-20', '06-27', '10-08', '10-15']
225.3 303.3 1.35
27 58
```

Altı gün üç olaya ait: her aykırı gün iki hata üretiyor, biri kendi gününde,
biri bir hafta sonra (tahmin o günü kopyalarken). 366 günün 6'sı MAE'yi
dörtte bir, RMSE'yi yarıdan fazla değiştiriyor. RMSE / MAE oranının 2'nin
üstünde olması tek başına bir uyarı: hataların arasında birkaç dev var.
