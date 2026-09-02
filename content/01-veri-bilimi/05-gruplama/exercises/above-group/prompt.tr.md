"Bu öğrenci kendi şehrinin ortalamasının üstünde mi?" sorusunu
cevaplayacaksın.

Bu soru `mean()` ile cevaplanamıyor: `mean()` grup başına **bir satır**
veriyor, senin ise her satırın yanında grubunun ortalaması gerekiyor.
`transform` tam bunun için var.

**Yapman gerekenler:**

1. Her satırın yanına kendi şehrinin ortalamasını yaz; sütunun adı
   `city_mean` olsun ve **bir basamağa yuvarlanmış** olsun.
2. Notu kendi şehrinin ortalamasının üstünde olanlar için `True` taşıyan
   `above` sütununu ekle.
3. `name`, `city`, `score`, `city_mean` ve `above` sütunlarını yazdır.
4. Kaç kişinin kendi şehrinin ortalamasının üstünde olduğunu yazdır.

**Beklenen çıktı:**

```
    name    city  score  city_mean  above
0    Ada  Ankara     82       87.0  False
1  Kerem   Izmir     74       71.3   True
2   Mina  Ankara     91       87.0   True
3  Deniz   Bursa     68       69.0  False
4    Efe  Ankara     88       87.0   True
5   Sila   Izmir     76       71.3   True
6   Kaan   Bursa     70       69.0   True
7    Ela   Izmir     64       71.3  False
5
```

**Aradaki fark:**

- `groupby(...).mean()` → 3 satır (grup sayısı). Tablo küçülüyor.
- `groupby(...).transform("mean")` → 8 satır (satır sayısı). Tablo aynı
  boyda kalıyor ve doğrudan sütun olarak eklenebiliyor.

Ada'ya dikkat: notu 82 ve genel ortalamanın üstünde, ama **kendi şehrinin**
ortalaması 87 olduğu için `False`. Gruplamanın anlamı burada görünüyor.
