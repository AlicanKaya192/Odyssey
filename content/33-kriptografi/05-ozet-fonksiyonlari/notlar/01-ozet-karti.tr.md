## Dört özellik

| Özellik | Anlamı |
|---|---|
| Belirlenimci | Aynı girdi → aynı özet |
| Tek yönlü | Özetten girdiye dönülemez |
| Çakışmaya dayanıklı | Aynı özetli iki girdi bulunamaz |
| Çığ etkisi | Bir bit değişince özetin yarısı değişir |

## Algoritmalar

| Ad | Bit | Durum |
|---|---|---|
| MD5 | 128 | Kırık |
| SHA-1 | 160 | Kırık |
| SHA-256 | 256 | Güvenli (SHA-2) |
| SHA-512 | 512 | Güvenli (SHA-2) |
| SHA-3 (sha3_256) | 256 | Güvenli |
| BLAKE2b | 512 | Güvenli, hızlı |

## Python kalıpları

- Onaltılık özet: `hashlib.sha256(veri).hexdigest()`.
- Ham bayt: `hashlib.sha256(veri).digest()`.
- Adıyla kurma: `hashlib.new("sha256")`, boyut `.digest_size`.
- Metni bayta: `"metin".encode()`; özet her zaman baytla çalışır.
- Bit farkı: `bin(int.from_bytes(a,"big") ^ int.from_bytes(b,"big")).count("1")`.

## Kullanım ve yanlış kullanım

| İş | Doğru | Yanlış |
|---|---|---|
| Dosya bütünlüğü | SHA-256 | MD5 (kırık) |
| Parola saklama | Yavaş tuzlu özet | Düz SHA-256 |
| Gönderen kanıtı + bütünlük | HMAC | Düz özet |
| Kopya tespiti | Herhangi bir özet | — |

## Akılda tutulacak

- Doğum günü sınırı: çakışma `2^(n/2)` denemeyle; 256 bit güvenli.
- Düz özet kasıtlı değişikliği durdurmaz, yalnızca kazara bozulmayı
  yakalar.
