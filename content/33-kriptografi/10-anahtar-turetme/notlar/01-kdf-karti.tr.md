## Üç tür girdi

| Girdi | KDF | Yavaş mı? | Tuz |
|---|---|---|---|
| Parola | Argon2id, scrypt, PBKDF2 | **Evet**, kasıtlı | Kişi başına rastgele |
| Güçlü ana sır | HKDF | Hayır | Uygulama başına sabit olabilir |
| Hiçbiri, yeni anahtar | `secrets.token_bytes(32)` | — | — |

## PBKDF2

```text
hashlib.pbkdf2_hmac("sha256", parola, tuz, tekrar, dklen=32)
```

- Tuz en az 16 bayt, `secrets.token_bytes(16)` ile, her kayıt için ayrı.
- Tekrar sayısı: SHA-256 ile yüz binlerce (örnek: 600 000); donanım
  hızlandıkça artırılır.
- Aynı parola + tuz + tekrar → hep aynı anahtar.

## scrypt

```text
hashlib.scrypt(parola, salt=tuz, n=2**14, r=8, p=1, dklen=32)
```

- `n`: maliyet (2'nin kuvveti), `r`: blok boyu, `p`: paralellik.
- Bellek yaklaşık `128 × r × n` bayt (bu ayarla 16 MB).

## HKDF

1. **Çek (extract):** `prk = HMAC(tuz, sır)`.
2. **Genişlet (expand):** `T(i) = HMAC(prk, T(i-1) + info + i)`, bloklar
   istenen uzunluğa kadar birleştirilir.
3. Her amaç için farklı `info`: `b"encryption"`, `b"mac"`, `b"v2-files"`.

## Saklanacaklar

Paroladan türetilmiş anahtarla şifrelenmiş bir dosyada şunlar şifreli
verinin yanında açıkça durur: **KDF adı, parametreleri (tekrar, n, r, p),
tuz**. Anahtarın kendisi hiçbir yere yazılmaz; her seferinde paroladan
yeniden türetilir.
