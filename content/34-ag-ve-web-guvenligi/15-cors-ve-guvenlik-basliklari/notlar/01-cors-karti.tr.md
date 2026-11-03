## CORS başlıkları

| Başlık | Kim gönderir | Ne der |
|---|---|---|
| `Origin` | Tarayıcı | İsteğin geldiği köken |
| `Access-Control-Allow-Origin` | Sunucu | Okumasına izin verilen köken (tek köken ya da `*`) |
| `Access-Control-Allow-Credentials` | Sunucu | `true`: çerezli istek okunabilir (`*` ile olmaz) |
| `Access-Control-Allow-Methods` | Sunucu (ön kontrol) | İzin verilen yöntemler |
| `Access-Control-Allow-Headers` | Sunucu (ön kontrol) | İzin verilen istek başlıkları |
| `Access-Control-Max-Age` | Sunucu (ön kontrol) | Ön kontrol cevabı kaç saniye saklanır |
| `Vary: Origin` | Sunucu | Cevap köken başına değişir, önbellek karıştırmasın |

## Sık hatalar

- Gelen `Origin`'i olduğu gibi geri yazmak (özellikle
  `Allow-Credentials: true` ile).
- Kökeni `endswith`, `startswith` ya da `in` ile denetlemek:
  `notshop.example`, `shop.example.other.example` gibi adlar geçer.
- `null` kökenine izin vermek.
- `http://` kökenine izin vermek: yoldaki biri o kökenin sayfasını
  değiştirebilir.
- `Vary: Origin` göndermemek.
- CORS'u bir erişim denetimi sanmak: CORS yalnızca **tarayıcıdaki
  betiğin** okumasını düzenler. Sunucuya doğrudan istek gönderen bir
  program CORS'a hiç takılmaz; yetkilendirme yine sunucuda yapılır.

## Doğru düzen

```text
1. Origin izin listesinde mi?  (tam eşitlik, küme)
2. Evet: Allow-Origin = o köken, gerekirse Allow-Credentials: true
3. Her durumda: Vary: Origin
4. Ön kontrolde: yalnızca gereken yöntem ve başlıklar
```
