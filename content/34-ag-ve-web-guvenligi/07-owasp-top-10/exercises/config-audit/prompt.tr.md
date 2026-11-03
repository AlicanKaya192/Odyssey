`config` sözlüğünde `debug`, `admin_password`, `dir_listing`,
`https_only` anahtarları var. `audit(config)` bulunan sorunların
kodlarını **şu sırayla** bir liste olarak döndürsün: `"debug"` (hata
ayıklama açık), `"default-password"` (parola `admin`, `password` ya da
`1234`), `"listing"` (klasör listeleme açık), `"http"` (`https_only`
kapalı).

**Beklenen çıktı:**

```
['debug', 'default-password', 'http']
[]
```
