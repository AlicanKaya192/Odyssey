`fill_median(rows)` sayı tablosundaki eksik değerleri (`None`) **medyanla**
doldursun ve her eksikli sütun için "eksikti" sütunu eklesin
(`SimpleImputer(strategy="median", add_indicator=True)`). Sonucu 2 basamağa
yuvarlı liste listesi döndürsün. Başlangıç kodu ortalamayla dolduruyor ve
işaret koymuyor.

**Beklenen çıktı:**

```
[1.0, 7.0, 0.0, 0.0]
[3.0, 8.0, 1.0, 0.0]
[3.0, 8.0, 0.0, 1.0]
[100.0, 9.0, 0.0, 0.0]
```
