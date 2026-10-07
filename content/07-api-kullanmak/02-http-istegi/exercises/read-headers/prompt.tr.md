İsteği gönderen program başlık adlarını farklı biçimlerde yazmış:
`Host`, `ACCEPT`, `user-agent`. Başlık adlarında büyük/küçük harf fark
etmediği için programda hepsini **küçük harfe** çevirip saklamak gerekiyor.

**Yapman gerekenler:**

1. `raw`'u satırlara böl. İlk satır istek satırı; geri kalanlar başlık.
2. Başlıkları `headers` adlı bir sözlükte, **adları küçük harfle** sakla.
   Değeri yalnızca **ilk** `": "` ayracından böl (`Host` değerinde de iki
   nokta var).
3. Ana makineyi, `Accept` değerini ve isteğin `Authorization` başlığı taşıyıp
   taşımadığını aşağıdaki gibi yazdır.

**Beklenen çıktı:**

```
host: localhost:8000
accept: application/json
has authorization: False
```
