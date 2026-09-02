Bir grup raporunda üç sütun bulunuyor: **kaç kişi, ortalama, yayılım.**
Üçünü birden çıkaracaksın.

**Yapman gerekenler:**

1. Şehre göre grupla ve `score` için sayı, ortalama ve standart sapmayı
   hesapla; iki ondalığa yuvarla.
2. Tabloyu yazdır.
3. Bütün verinin ortalamasını (iki ondalık) ve medyanını **yan yana**
   yazdır.
4. **En küçük grubun** adını yazdır.

**Beklenen çıktı:**

```
        count  mean    std
city
Ankara      3  80.0   9.17
Bursa       2  48.0   4.24
Izmir       3  79.0  15.13
71.62 76.0
Bursa
```

**Çıktıyı oku:**

- Bursa'nın ortalaması düşük ama **iki kişi var**; bir sonuç değil.
- Izmir'in `std` değeri 15.13, Ankara'nınki 9.17. Aynı ortalamaya yakın iki
  grup, ama Izmir çok daha dağınık — orada birbirinden farklı iki tip
  öğrenci olabilir.
- Genel ortalama 71.62, medyan 76. Ortalama medyandan küçük, yani aşağıda
  düşük notlar var.

Üç satırlık bir kod, üç ayrı bulgu. `agg` bu yüzden tek tek çağrılara
tercih ediliyor.
