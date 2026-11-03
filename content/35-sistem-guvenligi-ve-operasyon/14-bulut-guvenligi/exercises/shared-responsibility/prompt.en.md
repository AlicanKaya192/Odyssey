The starter code has the layers (`LAYERS`, from customer to provider) and,
for each model, the index where the provider's responsibility starts
(`PROVIDER_FROM`). `responsibility(model, layer)` should return
`"customer"` if the layer's index is smaller than `PROVIDER_FROM[model]`,
otherwise `"provider"`. If the model or layer is unknown, `"unknown"`.

**Expected output:**

```
IaaS operating system -> customer
PaaS operating system -> provider
SaaS data -> customer
SaaS kitchen -> unknown
```
