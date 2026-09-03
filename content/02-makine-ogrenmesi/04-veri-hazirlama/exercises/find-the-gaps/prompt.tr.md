Bu bölümün dosyası öncekiler gibi temiz değil. Model kurmadan önce neyle
uğraşacağını görmen gerekiyor.

`cars.csv` dosyasında 120 araba var; sütunlar `age`, `km`, `engine`, `fuel`,
`gearbox`, `price`.

**Yapman gerekenler:**

1. Dosyayı oku ve kaç satır olduğunu yazdır.
2. **Eksik değeri olan** sütunları bul. Her biri için `sutun:sayi` biçiminde
   bir metin üret ve listeyi yazdır. Eksiği olmayan sütunlar listeye
   girmesin.
3. **Metin sütunlarının** adlarını liste hâlinde yazdır.
4. `fuel` sütunundaki farklı değerleri **sıralı** olarak yazdır.

**Beklenen çıktı:**

```
120
['engine:14']
['fuel', 'gearbox']
['diesel', 'lpg', 'petrol']
```

**Üç bulgu, üç sorun:**

- **`engine` sütununun 14 satırı boş.** sklearn eksik değerle çalışmıyor;
  `ValueError: Input contains NaN` alırsın.
- **İki sütun metin.** Model sayıyla çalışıyor;
  `could not convert string to float: 'diesel'` alırsın.
- **`fuel`'da üç kategori var ve aralarında sıra yok.** `petrol=0, diesel=1,
  lpg=2` demek modele olmayan bir sıra öğretmek olurdu.

Sonraki alıştırmalar bu üçünü sırayla çözüyor.

**Bir uyarı:** metin sütunlarını bulmak için birçok kaynakta
`df.dtypes == "object"` geçiyor. pandas 3'te metin sütunları artık `object`
değil ve o kontrol **boş liste** veriyor. Çalışan yol
`select_dtypes(exclude="number")` — "sayı olmayan sütunlar".
