Bir web sitesinden sayfa çekmeyi taklit eden bir fonksiyonu iş parçacığı
havuzuyla çalıştır.

**Yapman gerekenler:**

1. `fetch(page)` fonksiyonunu yaz: `time.sleep(0.1)` ile beklesin ve
   `page * 10` döndürsün (sayfadaki ürün sayısı gibi düşün).
2. `ThreadPoolExecutor(max_workers=8)` ile `fetch`'i 1'den 8'e kadar
   sayfalar için çalıştır (`ex.map`), sonuçları listeye al.
3. Listeyi ve toplamını ayrı satırlara yazdır.

**Beklenen çıktı:**

```
[10, 20, 30, 40, 50, 60, 70, 80]
360
```

Sekiz bekleme aynı anda yapıldığı için iş yaklaşık 0,1 saniye sürüyor;
sıralı olsaydı 0,8 saniye sürerdi.
