Bölümleme hataları çoğu zaman hemen görünmüyor: kod çalışıyor, sonuç yanlış
ya da yavaş çıkıyor.

## 1. Çok ince bölmek

Güne göre 366 dosyayı okumak tek dosyadan on beş kat yavaştı. Müşteriye göre
bölmek 245 461 klasör demek. Az değerli bir sütun seç; çok değerli sütun için
kova kullan.

## 2. Ayları sıfırsız yazmak

Klasör adları metin olarak karşılaştırılıyor:

```python
"2024-10" < "2024-9"     # True
"2024-10" < "2024-09"    # False
```

Metin karşılaştırması karakter karakter gidiyor ve `1`, `9`'dan önce
geliyor. Ayı her zaman iki haneli yaz: `strftime("%Y-%m")` bunu kendisi
yapıyor.

## 3. `exist_ok=True`'yu unutmak

```python
folder.mkdir(parents=True)          # klasör varsa FileExistsError
folder.mkdir(parents=True, exist_ok=True)
```

İkinci çalıştırmada klasör zaten var; `exist_ok=True` olmadan kod düşüyor.

## 4. Bölüm sütununu hem adda hem dosyada tutmak

Sütunu dosyaya da yazarsan iki kaynak oluyor ve biri değişince (klasörü
yeniden adlandırmak gibi) birbirini tutmuyorlar. Bölüm sütununu dosyadan
çıkar (`drop(columns=...)`); okurken adından geri koy.

## 5. Adından geri konan sütunun türünü unutmak

Klasör adından gelen değer **metin**: `"2024-03"`. Sayı ya da tarih
gerekiyorsa çevir (`int(...)`, `pd.to_datetime(...)`). `partition_cols` ile
okurken pandas bu sütunu `category` yapıyor.

## 6. Yeni veride her şeyi yeniden yazmak

Yeni ay geldiğinde bütün klasörleri silip baştan yazmak gereksiz; yalnızca
yeni ayın klasörünü ekle. Eski bir ayı düzeltmek gerekiyorsa yalnızca o
klasörü yeniden yaz.

## 7. Aynı klasöre iki kez yazıp eski dosyayı unutmak

`partition_cols` her yazışta rastgele adlı yeni dosyalar açıyor. Aynı veriyi
aynı klasöre ikinci kez yazarsan eski dosyalar da kalıyor ve okurken her
satır iki kez geliyor. Yeniden yazmadan önce eski klasörü temizle.

## 8. Bölüm değerinde `/` ya da garip karakterler

`category=home/garden` gibi bir değer klasör yolunu böler. Bölüm değerlerini
sade tut (harf, rakam, `-`, `_`).
