Bir anahtarın hangi reduce makinesine gideceğini her süreçte aynı
cevabı verecek şekilde hesaplayan fonksiyonu yaz.

**Yapman gerekenler:**

`partition(key, reducers)` fonksiyonunu yaz:

- Anahtarı bayta çevir: `key.encode()`.
- Kararlı karmasını al: `zlib.crc32(...)`.
- Makine sayısına bölümden kalanı döndür: `% reducers`.

Python'un `hash()`'ini kullanma: metin karması her süreçte farklı.

Örnek: `partition("Istanbul", 4)` → `1`.
