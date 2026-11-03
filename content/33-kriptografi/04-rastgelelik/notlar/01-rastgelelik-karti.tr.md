## İki üreteç

| | `random` | `secrets`, `os.urandom` |
|---|---|---|
| Tür | Sözde rastgele (PRNG) | Kriptografik (CSPRNG) |
| Kaynak | Tohum + formül | İşletim sisteminin gürültü kaynağı |
| Aynı tohum | Aynı dizi | Tohum yok |
| Kullanım | Benzetim, oyun, örneklem | Anahtar, nonce, tuz, jeton, parola |

## `secrets` fonksiyonları

| Çağrı | Verdiği | Örnek iş |
|---|---|---|
| `token_bytes(n)` | `n` rastgele bayt | Anahtar, nonce, tuz |
| `token_hex(n)` | `n` bayt, `2n` onaltılık karakter | Jeton, API anahtarı |
| `token_urlsafe(n)` | `n` bayt, Base64 (bağlantıya uygun) | Parola sıfırlama bağlantısı |
| `randbelow(n)` | `0` … `n - 1` arası tam sayı | Doğrulama kodu |
| `choice(dizi)` | Diziden bir öğe | Parola karakteri |

`os.urandom(n)` de `n` rastgele bayt verir; `token_bytes` ile aynı
kaynaktır.

## Boyutlar

| Değer | Bayt | Bit |
|---|---|---|
| AES-256 anahtarı | 32 | 256 |
| AES-GCM nonce | 12 | 96 |
| Tuz | 16 | 128 |
| Uzun ömürlü jeton | en az 16 | en az 128 |

## Entropi

- Rastgele seçilmiş `n` karakter, `a` harflik alfabe: `n × log2(a)` bit.
- Alfabede aynı harf iki kez yazılsa da olasılık artmaz: `a` **farklı**
  karakter sayısıdır.
- 128 bit için gereken uzunluk: `math.ceil(128 / math.log2(a))`.

| Alfabe | Karakter başına bit | 128 bit için |
|---|---|---|
| 10 rakam | 3,32 | 39 karakter |
| 16 onaltılık | 4 | 32 karakter |
| 62 harf ve rakam | 5,95 | 22 karakter |
| 64 Base64 | 6 | 22 karakter |

## Modulo yanlılığı

- `bayt % 100`: 0–55 sonuçları 256'da 3 kez, 56–99 sonuçları 2 kez çıkar.
- Doğrusu: `256 - 256 % n` sınırının üstünü at, yeniden çek.
- Python'da bunu `secrets.randbelow(n)` yapar; elle yazma.
