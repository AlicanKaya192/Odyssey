## Doğrulama sırası

1. **Kanonik biçim:** `unicodedata.normalize("NFKC", s).strip()`, gerekiyorsa
   `casefold()`.
2. **Tür:** sayı mı, tarih mi? Önce biçim denetimi, sonra dönüştürme.
3. **Biçim:** `re.fullmatch(desen, s)` ile izin verilen karakterler ve
   uzunluk.
4. **Aralık ya da küme:** `13 <= yas <= 120`, `ulke in ULKELER`.
5. **Reddet:** biri tutmazsa veri kullanılmaz; kullanıcıya hangi alanın
   hatalı olduğu söylenir (ama iç ayrıntı değil).

## Python kalıpları

| İş | Kalıp |
|---|---|
| Tam eşleşme | `re.fullmatch(r"[a-z0-9_]{3,20}", s)` |
| Yalnızca ASCII rakam | `re.fullmatch(r"[0-9]{1,3}", s)` (`isdigit` üst simgeyi de kabul eder) |
| Küme | `s in IZINLI` |
| Kanonik | `unicodedata.normalize("NFKC", s).strip().casefold()` |
| Güvenli yol | `posixpath.normpath(posixpath.join(BASE, ad))` + `startswith(BASE + "/")` |
| Komut | Argüman listesi; gerekirse `shlex.quote(deger)` |

## Bağlama göre kodlama

| Bağlam | Kodlayıcı |
|---|---|
| HTML | `html.escape` |
| Adres parametresi | `urllib.parse.quote(s, safe="")` |
| JSON | `json.dumps` |
| SQL | Parametreli sorgu (kodlama değil) |
| Kabuk komutu | Argüman listesi, `shlex.quote` |

## Kurallar

- Doğrulama **sunucuda**; tarayıcıdaki yalnızca kolaylık.
- **İzin listesi**, kara liste değil.
- Önce kanonik biçim, sonra doğrulama.
- Doğrulama kodlamanın yerini tutmaz; ikisi birlikte.
