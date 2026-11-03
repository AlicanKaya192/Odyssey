`random_source(purpose)` bir değerin hangi modülle üretilmesi
gerektiğini söylesin: `purpose` `"token"`, `"key"`, `"password"`,
`"nonce"` ya da `"salt"` ise `"secrets"`, değilse (oyun, benzetim)
`"random"`. Başlangıç kodu her şeye `"random"` diyor.

**Beklenen çıktı:**

```
token secrets
dice random
salt secrets
simulation random
```
