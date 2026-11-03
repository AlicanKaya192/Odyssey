Başlangıç kodunda katmanlar (`LAYERS`, müşteriden sağlayıcıya) ve her
modelde sağlayıcının sorumluluğunun başladığı sıra (`PROVIDER_FROM`) var.
`responsibility(model, layer)` katmanın sırası `PROVIDER_FROM[model]`'den
küçükse `"customer"`, değilse `"provider"` döndürsün. Model ya da katman
bilinmiyorsa `"unknown"`.

**Beklenen çıktı:**

```
IaaS operating system -> customer
PaaS operating system -> provider
SaaS data -> customer
SaaS kitchen -> unknown
```
