Geçme notu 75'e çekildi: bunun altında kalan herkesin notu 75 yapılacak.

**Yapman gerekenler:**

1. Notu **75'in altında** olan satırların `score` değerini `75` yap.
2. `name` ve `score` sütunlarını yazdır.
3. Kaç kişinin notunun tam 75 olduğunu yazdır.
4. Yeni not ortalamasını (iki basamağa yuvarlanmış) yazdır.

**Beklenen çıktı:**

```
    name  score
0    Ada     82
1  Kerem     75
2   Mina     91
3  Deniz     75
4    Efe     88
5   Sila     76
2
81.17
```

**Bu alıştırmanın asıl konusu şu:** aşağıdaki satır **hiçbir şey yapmıyor.**

```python
data[data["score"] < 75]["score"] = 75
```

Köşeli parantez ara bir tablo üretiyor, atama ona gidiyor, o tablo da hemen
çöpe atılıyor. Hata da almıyorsun — kod çalışıyor ve tablo değişmemiş
oluyor.

Doğrusu seçim ve atamayı **tek bir `loc` çağrısında** yapmak. Kural şu:
tabloyu değiştirecekseniz köşeli parantezi iki kez üst üste kullanmayın.
