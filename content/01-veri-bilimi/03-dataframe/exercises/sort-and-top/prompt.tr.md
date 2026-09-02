Sıralama yaptığında index'e ne olduğunu göreceksin — pandas'ta en çok
şaşırtan davranışlardan biri.

**Yapman gerekenler:**

1. Tabloyu nota göre **büyükten küçüğe** sırala, sonucu `ranked` adlı
   değişkende tut.
2. `ranked` tablosunun `name` ve `score` sütunlarının **ilk üç satırını**
   yazdır.
3. En yüksek notu alanın adını yazdır — bunu **sıralamadan bağımsız**, `data`
   üzerinden `idxmax()` ile bul.
4. `ranked` tablosunun index'ini liste hâlinde yazdır.

**Beklenen çıktı:**

```
   name  score
2  Mina     91
4   Efe     88
0   Ada     82
Mina
[2, 4, 0, 1, 3]
```

**Son satıra dikkat:** index `[0, 1, 2, 3, 4]` değil `[2, 4, 0, 1, 3]`.
Satırlar yer değiştirdi ama **etiketleri onlarla birlikte taşındı**. Bu iyi
bir şey — hangi satırın nereden geldiğini kaybetmiyorsun — ama sıralanmış
bir tabloyu başka bir tabloyla birleştireceksen bu delikli index sürpriz
`NaN`'lar üretebiliyor.

Numaraları sıfırlamak istersen: `ranked.reset_index(drop=True)`.
