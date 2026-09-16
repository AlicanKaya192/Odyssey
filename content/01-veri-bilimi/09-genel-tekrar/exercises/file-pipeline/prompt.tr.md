Modülün tamamı bu alıştırmada: kirli bir dosyayı okuyup temizleyecek
ve özetleyeceksin. **Kaç kayıtla başlayıp kaçıyla bittiğini** de
raporlayacaksın.

Dosyanın tamamı (`results_raw.csv`):

```text
id,city,score
1,Ankara,82
2,Izmir ,74
3,ankara,91
4,Bursa,
5,Izmir,68
5,Izmir,68
6,ANKARA,abc
7,bursa ,77
8,Adana,85
```

**Yapman gerekenler:**

1. İçe aktarmayı yaz, dosyayı `raw` adıyla oku ve bir kopya al.
2. `city` sütununu temizle: kenar boşluklarını at, baş harfleri büyük olsun.
3. `score` sütununu sayıya çevir — çevrilemeyen değer boş olsun.
4. Kaç satırla başladığını bir değişkende tut.
5. `id`'ye göre tekrar eden kayıtları at, kalan satır sayısını tut.
6. Notu boş olan kaç kayıt kaldığını say, sonra o satırları at.
7. Dört sayıyı **tek satırda yan yana** yazdır: başlangıç, tekrarsız, eksik,
   kalan.
8. Şehre göre kayıt sayısını ve ortalamayı (bir ondalık) **ayrı ayrı
   sözlük** olarak yazdır.

**Beklenen çıktı:**

```
9 8 2 6
{'Adana': 1, 'Ankara': 2, 'Bursa': 1, 'Izmir': 2}
{'Adana': 85.0, 'Ankara': 86.5, 'Bursa': 77.0, 'Izmir': 71.0}
```

**Dikkat edilecek üç şey:**

- **Sıra:** şehri düzeltmeden gruplarsan `Izmir ` ile `Izmir`, `ankara` ile
  `ANKARA` ayrı gruplar olur.
- **`abc` bir hata değil, veriden gelen kirlilik.** `errors="coerce"` onu
  boşa çevirip programı yürütüyor.
- **Sayılar rapora girer.** Dokuz satırla başlayıp altıyla bitirdin. Bunu
  yazmayan bir analiz, okuyanın bilmesi gereken bir şeyi saklıyor.

Son sözlüklere bak: **Bursa'nın ortalaması tek bir öğrenciye dayanıyor** —
iki kaydından biri boştu. Adana'da da tek kayıt var. "Adana 85 ortalamayla
ikinci" demek teknik olarak doğru, ama tek bir notun sıralaması güvenilir
değil.
