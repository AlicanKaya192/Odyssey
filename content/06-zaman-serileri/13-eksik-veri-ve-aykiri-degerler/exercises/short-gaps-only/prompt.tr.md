`machine_log.csv` bir makinenin sıcaklık sensörü (`time`, `temp_c`).
Ölçümler düzensiz aralıklarla geliyor ve 7 Mayıs gecesi sensör saatlerce
susuyor. Veriyi 10 dakikalık ızgaraya oturt; kısa boşlukları doldur, arızaya
dokunma.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli oku ve `temp_c` sütununu 10 dakikalık ortalamaya
   çevir: `r = x.resample("10min").mean()`.
2. `r`'nin uzunluğunu ve `NaN` sayısını aynı satıra yazdır.
3. Boşlukların uzunluklarını bul (`(missing != missing.shift()).cumsum()`
   sayacı). Boşluk **sayısını**, en uzun boşluğun uzunluğunu ve 3 hücre ya da
   daha kısa olan boşluklardaki toplam hücre sayısını aynı satıra yazdır.
4. Yalnızca 3 hücre ya da daha kısa boşlukları doğrusal doldur:
   her satır için içinde bulunduğu boşluğun uzunluğunu
   `missing.groupby(run_id).transform("sum")` ile bul,
   `short = missing & (run_length <= 3)` maskesini kur ve
   `result = r.where(~short, r.interpolate())` yaz.
5. `result`'ta kalan `NaN` sayısını yazdır.
6. Karşılaştırma için `r.interpolate(limit=3)` sonrasında kalan `NaN` sayısını
   yazdır.

**Beklenen çıktı:**

```
432 54
22 33 21
33
30
```

Kısa boşlukların hepsi doldu, arızanın 33 hücresi olduğu gibi kaldı.
`interpolate(limit=3)` ise arızanın ilk üç hücresini de doldurdu: 33 yerine 30
boş hücre. `limit` "kısa boşluklar" demek değil, "her boşluktan en çok üç"
demek.
