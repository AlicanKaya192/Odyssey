Üç öğrenci, üç sınav. Notlar tek sıra hâlinde elinde; onu tabloya çevirip
iki yönde de hesap yapacaksın.

`flat` dizisi öğrenci öğrenci sıralı: ilk üç sayı birinci öğrencinin üç
sınavı, sonraki üç sayı ikinci öğrencinin, ve böyle devam ediyor.

**Yapman gerekenler:**

1. `flat` dizisini **3 satır 3 sütun** hâline getir, adı `matrix` olsun.
2. Her **öğrencinin** toplam notunu hesapla, `per_student` adlı diziye koy.
3. Her **sınavın** ortalamasını hesapla, `per_exam` adlı diziye koy.
4. En yüksek toplamı yapan öğrencinin **sırasını** bul, `best` adlı
   değişkende tut.
5. Sırayla yazdır: `matrix`, `per_student`, iki basamağa yuvarlanmış
   `per_exam`, `best`.

**Beklenen çıktı:**

```
[[12 15  9]
 [20 18 11]
 [14 17 13]]
[36 49 44]
[15.33 16.67 11.  ]
1
```

**Asıl mesele:** hangisi `axis=0`, hangisi `axis=1`? Satırlar öğrenci
olduğuna göre "öğrenci başına toplam" satır boyunca gidiyor. Karıştırırsan
çıktının şekli tutmuyor — orası sana söylüyor.
