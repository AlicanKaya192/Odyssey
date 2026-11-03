`pad(data_hex, block)` onaltılık veriye PKCS#7 dolgusu eklesin ve
sonucu onaltılık döndürsün. Önce `bytes.fromhex`; eksik bayt sayısı
`need = block - (len(data) % block)`; `need` tane, her biri `need`
değerinde bayt eklenir. Veri tam blok katıysa da **yeni bir tam blok**
eklenir (`need` 0 değil `block` olur).

**Beklenen çıktı:**

```
5 -> 16 last: 11
16 -> 32 last: 16
```
