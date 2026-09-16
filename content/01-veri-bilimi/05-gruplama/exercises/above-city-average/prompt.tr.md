"Bu öğrenci **kendi şehrinin** ortalamasının üstünde mi?" sorusunu
dosyadaki veriyle cevaplayacaksın.

Veri `students.csv` dosyasında:

```text
name,city,age,hours,score
Ada,Ankara,21,12,82
Kerem,Izmir,23,6,74
Mina,Ankara,22,14,91
Deniz,Bursa,25,4,68
Efe,Ankara,21,11,88
Sila,Izmir,24,8,76
...
```

Bu soru `mean()` ile cevaplanamıyor: `mean()` grup başına **bir satır**
veriyor, senin ise her satırın yanında grubunun ortalaması gerekiyor.
`transform` tam bunun için var.

**Yapman gerekenler:**

1. İçe aktarmayı yaz ve dosyayı oku.
2. Şehir ortalamalarını bir ondalığa yuvarlayıp **sözlük olarak** yazdır.
3. Her satırın yanına kendi şehrinin ortalamasını yaz; sütunun adı
   `city_mean`, bir ondalığa yuvarlanmış.
4. Notu kendi şehrinin ortalamasının üstünde olanlar için `True` taşıyan
   `above` sütununu ekle.
5. Kendi şehrinin üstünde olanların adlarını **liste olarak**, sonra
   sayılarını yazdır.

**Beklenen çıktı:**

```
{'Adana': 82.0, 'Ankara': 85.2, 'Bursa': 70.0, 'Izmir': 71.3}
['Kerem', 'Mina', 'Efe', 'Sila', 'Zeynep', 'Can']
6
```

**Aradaki fark:**

- `groupby(...).mean()` → 4 satır (şehir sayısı). Tablo küçülüyor.
- `groupby(...).transform("mean")` → 12 satır. Tablo aynı boyda kalıyor ve
  doğrudan sütun olarak eklenebiliyor.

**Ada'ya bak:** notu 82, bütün sınıfın ortalamasının (77.42) üstünde. Ama
listede yok, çünkü **kendi şehrinin** ortalaması 85.2. Gruplamanın anlamı
burada görünüyor.
