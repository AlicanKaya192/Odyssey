Animal Farm'ın (12 numara) fiyatı indirime girdi. Yalnızca fiyatı değiştir
ve sonucu doğrula.

**Yapman gerekenler:**

1. Önce kitabı `GET` ile oku ve eski fiyatı yazdır.
2. `PATCH /books/12` ile yalnızca `{"price": 5.5}` gönder; durum kodunu
   yazdır.
3. Kitabı yeniden `GET` ile oku; yeni fiyatı ve yılın değişmediğini
   göstermek için yılı yazdır.

**Beklenen çıktı:**

```
old price: 6.9
patch: 200
new price: 5.5
year: 1945
```
