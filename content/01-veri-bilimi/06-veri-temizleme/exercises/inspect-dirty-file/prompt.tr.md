Temizliğe başlamadan önce **bakıyorsun**. Bu dosya bilerek kirli
bırakıldı; beş satırlık bir incelemeyle sorunların çoğunu yakalayacaksın.

Dosyanın tamamı (`students_raw.csv`):

```text
id,name,city,score
1, Ada ,Ankara,82
2,kerem,izmir ,74
3,MINA,ANKARA,91
3,MINA,ANKARA,91
4,Deniz,bursa,
5,efe ,IZMIR,abc
6,Sila,,76
7,Kaan,Bursa,-1
```

**Yapman gerekenler:**

1. İçe aktarmayı yaz ve dosyayı `raw` adıyla oku.
2. Tablonun boyutunu yazdır.
3. Sütun tiplerini okunur bir liste olarak yazdır.
4. Toplam kaç **eksik hücre** olduğunu yazdır.
5. Kaç satırın **birebir tekrar** olduğunu yazdır.
6. `city` sütununda kaç **farklı yazım** olduğunu yazdır.

**Beklenen çıktı:**

```
(8, 4)
['int64', 'str', 'str', 'str']
2
1
6
```

**Her sayı bir sorunu işaret ediyor:**

- **`score` metin çıktı.** Sütunda `abc` var; tek bir bozuk değer bütün
  sütunu metne çeviriyor, ortalama alamazsın. Tipi düzeltmek gerekecek.
- **İki eksik hücre:** Deniz'in notu ve Sila'nın şehri boş. `read_csv` boş
  hücreyi `NaN` yapıyor.
- **Bir tekrar:** Mina iki kez yazılmış.
- **Farklı yazım sayısı, gerçek şehir sayısından fazla.** `Ankara`, `ANKARA`,
  `izmir ` (sonunda boşluk) — bilgisayar için hepsi ayrı değer. Gruplamadan
  önce düzeltilmezse aynı şehir birkaç gruba bölünür.

Bir de gözle görülüp sayıyla görülmeyen şey var: Kaan'ın notu `-1`. Tip
doğru, hücre dolu, ama değer imkânsız. Aykırı değerler başlığı bunun için.
