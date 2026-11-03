`pad` hazır. `unpad(data_hex)` PKCS#7 dolgusunu çıkarıp sonucu
onaltılık döndürsün: `bytes.fromhex` ile baytı al, son bayt kaç dolgu
baytı eklendiğini söyler, o kadar baytı sondan at. İpucu:
`data[:-data[-1]]`.

**Beklenen çıktı:**

```
True
True
```
