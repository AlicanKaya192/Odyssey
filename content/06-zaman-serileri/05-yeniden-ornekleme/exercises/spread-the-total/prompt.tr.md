Elinde yalnızca aylık toplamlar olduğunu düşün ve onları günlüğe aç:
önce yanlış yoldan, sonra doğru yoldan.

**Yapman gerekenler:**

1. `store_sales.csv` dosyasını oku; 2024'ün aylık toplamlarını ay başı
   etiketiyle hesapla: `s.loc["2024"].resample("MS").sum()`.
2. **Yanlış yol:** `monthly.resample("D").ffill()`. Satır sayısını ve son
   tarihi (`"%Y-%m-%d"`) aynı satıra yazdır.
3. Yanlış serideki Mart toplamını yazdır.
4. **Doğru yol:** her ayın toplamını gün sayısına böl
   (`monthly / monthly.index.days_in_month`), 2024'ün bütün günlerinden
   oluşan bir indeks kur (`pd.date_range`) ve `reindex(idx, method="ffill")`
   ile günlere yay.
5. Doğru serideki Mart toplamını bir ondalığa yuvarlayıp yazdır.
6. 9 Mart 2024 için paylaştırılmış değeri (bir ondalık) ve gerçek satışı aynı
   satıra yazdır.

**Beklenen çıktı:**

```
336 2024-12-01
276489
8919.0
287.7 384
```

Yanlış yolda iki hata birden var: Aralık'ın 30 günü kayıp ve Mart 31 kat
şişmiş. Doğru yolda aylık toplam tutuyor, ama son satıra bak: cumartesi günü
için ayın ortalaması yazıyor. Aylık veride haftanın günleri yok; sıklaştırmak
onları geri getirmiyor.
