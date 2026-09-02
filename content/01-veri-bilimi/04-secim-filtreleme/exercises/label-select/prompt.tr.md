`loc` sıraya değil **etikete** bakıyor. Bu alıştırmada aradaki en önemli
farkı göreceksin.

**Yapman gerekenler:**

1. `name` sütununu index yapan `by_name` tablosunu üret.
2. Mina'nın notunu yazdır.
3. `Ada` ile `Mina` **arasındaki** satırların notlarını yazdır.
4. Kerem'in şehrini yazdır.
5. Üçüncü adımdaki seçimin **kaç satır** olduğunu yazdır.

**Beklenen çıktı:**

```
91
name
Ada      82
Kerem    74
Mina     91
Name: score, dtype: int64
Izmir
3
```

**Son satır bu alıştırmanın bütün mesele:** `"Ada":"Mina"` **üç** satır
veriyor, Mina da içeride. `iloc[0:2]` olsaydı iki satır gelirdi.

`loc` bitişi içeri alıyor çünkü etiketlerle çalışırken "Mina'dan bir
önceki" demek anlamsız — etiketlerin sayısal bir sırası olmayabiliyor.
