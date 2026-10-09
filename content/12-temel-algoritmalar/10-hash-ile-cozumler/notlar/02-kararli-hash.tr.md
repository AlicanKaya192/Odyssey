Python'un `hash()`'i bir süreç içinde güvenilir, ama metinlerde **her
çalıştırmada değişir**. Değeri dosyaya yazmak, iki programın aynı sonucu
vermesini beklemek ya da veriyi sabit biçimde parçalara bölmek için
**kararlı** bir hash gerekir.

## `zlib.crc32`: hızlı ve kararlı

```python
import zlib

key = "Istanbul"
print(zlib.crc32(key.encode("utf-8")))          # her çalıştırmada aynı sayı
print(zlib.crc32(key.encode("utf-8")) % 4)      # 4 parçadan hangisi?
```

Büyük Veri patikasında veriyi işçilere dağıtırken bunu kullandık. Hızlı ama
**güvenlik için değil**: kasıtlı olarak aynı değeri veren iki metin bulmak
kolaydır.

## `hashlib`: parmak izi

```python
import hashlib

content = "merhaba dunya".encode("utf-8")
print(hashlib.sha256(content).hexdigest()[:16])   # 64 karakterin ilk 16'sı
```

SHA-256 iki farklı içeriğin aynı sonucu vermesini pratikte imkânsız kılar.
Kullanım: dosyanın değişip değişmediğini anlamak (Odyssey'nin güncelleme
kayıtları da her dosyanın SHA-256'sını tutar), tekrar eden dosyaları bulmak,
indirilen dosyayı doğrulamak.

## Hangisi ne zaman?

| İhtiyaç | Araç |
|---|---|
| Bir süreç içinde küme/sözlük | yerleşik `hash()` (kendiliğinden) |
| Veriyi sabit biçimde `n` parçaya bölmek | `zlib.crc32(...) % n` |
| İçeriğin parmak izi, bütünlük denetimi | `hashlib.sha256` |
| Parola saklamak | hiçbiri tek başına değil: tuzlu, yavaş özel fonksiyonlar (`hashlib.pbkdf2_hmac`; API Yazmak modülünde kullandık) |

**Not:** `hashlib` ve `crc32` metin değil **bayt** ister; `encode("utf-8")`
unutulursa `TypeError` alınır.
