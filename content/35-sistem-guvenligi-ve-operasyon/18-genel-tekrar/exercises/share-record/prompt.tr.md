`share_record(record, allowed, key)` kaydı başka bir ekiple paylaşmak
için hazırlasın: yalnızca `allowed` alanları kalsın, `email` kaldıysa
`strip().lower()` ile normalleştirilip `hmac.new(key.encode(), ...,
hashlib.sha256)` özetinin ilk 12 karakteriyle takma ada çevrilsin. Başlangıç
kodu anahtarsız düz özet kullanıyor. Gizlilik ve Veri Koruma, Sır
Yönetimi.

**Beklenen çıktı:**

```
email 5e979343af4e
plan pro
```
