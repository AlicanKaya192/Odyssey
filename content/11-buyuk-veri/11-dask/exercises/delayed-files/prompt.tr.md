Her dosyanın cirosunu hesaplayan bir fonksiyonu `delayed` ile tembel ve
paralel çalıştır.

**Yapman gerekenler:**

1. Başlangıç kodu dört CSV dosyasını yazıyor.
2. `file_revenue(path)` fonksiyonunu yaz: dosyayı pandas ile okusun ve
   `quantity * unit_price` toplamını döndürsün.
3. Dört dosya için `delayed(file_revenue)(yol)` tariflerini bir listeye
   koy; `total = delayed(sum)(parts)`.
4. `total`'ın türünün adını yazdır.
5. `total.compute()` sonucunu iki ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
Delayed
327426855.28
```
