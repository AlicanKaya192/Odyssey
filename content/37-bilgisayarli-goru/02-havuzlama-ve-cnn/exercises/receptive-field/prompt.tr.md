`receptive_field(layers)` `[çekirdek, adım]` çiftlerinden oluşan bir katman
listesinin son katmanındaki alıcı alanı döndürsün. Başlangıçta alan 1,
atlama 1; her katmanda alan `(çekirdek - 1) * atlama` kadar büyür, sonra
atlama adımla çarpılır.

**Beklenen çıktı:**

```
5
18
19
```
