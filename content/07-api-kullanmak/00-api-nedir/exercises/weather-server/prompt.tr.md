Gerçek API'ler yanıtı düz bir metin olarak değil, **durum + veri**
olarak döndürüyor. Durum, isteğin başarılı olup olmadığını söyleyen sayı:
`200` başarılı, `404` bulunamadı.

**Yapman gerekenler:**

1. `server(city)` fonksiyonunu yaz:
   - şehir `temps` sözlüğündeyse `{"status": 200, "temp": <sıcaklık>}`,
   - değilse `{"status": 404, "error": "unknown city"}` döndürsün.
2. İstemci kısmı: `cities` listesindeki her şehir için `server`'ı çağır.
   Durum `200` ise `Istanbul: 18`, değilse `Paris: error 404 (unknown city)`
   biçiminde yazdır.

**Beklenen çıktı:**

```
Istanbul: 18
Paris: error 404 (unknown city)
Izmir: 22
```

İstemci yanıtın içine bakmadan önce **durumu** kontrol ediyor. Gerçek
API'lerle çalışırken de ilk iş bu: yanıt başarılı mı?
