Temizliğin son iki adımı: tekrarları atmak ve eksik notlarla ne yapacağına
karar vermek.

Başlangıç kodunda adlar, metinler ve tipler zaten temizlendi.

**Yapman gerekenler:**

1. `name` sütununa göre kaç tekrar eden satır olduğunu yazdır.
2. `name` sütununa göre tekrarları at, sonra notu eksik olan satırları at.
   Index'i sıfırla ve sonucu `clean` adlı tabloda tut.
3. `clean` tablosunun şeklini yazdır.
4. `clean` tablosunu yazdır.
5. Temizlenmiş verinin not ortalamasını (iki basamağa yuvarlanmış) yazdır.

**Beklenen çıktı:**

```
1
(4, 3)
    name    city  score
0    Ada  Ankara   82.0
1  Kerem   Izmir   74.0
2   Mina  Ankara   91.0
3    Efe   Izmir   88.0
83.75
```

**İki şeye dikkat:**

- **Tekrar ancak metin temizlendikten sonra görünüyor.** İlk alıştırmada
  `duplicated()` sıfır demişti, çünkü biri `"Ada "` ötekisi `" Ada "` idi.
  Sıra önemli.
- `dropna(subset=["score"])` yazdık, çıplak `dropna()` değil. Çıplak hâli
  **herhangi bir** sütunu boş olan satırı atıyor; yirmi sütunlu bir tabloda
  bu, verinin yarısını kaybetmek demek.

Yedi satırla başladın, dördüyle bitirdin. Üç satırı kaybettin ve **bunu
raporunda söylemen gerekiyor** — hangi kararla kaç kayıt gitti.
