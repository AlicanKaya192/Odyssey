`schema(tools)` araç sözlüğünden modele gidecek listeyi kursun: her araç
için `{"name": ad, "description": açıklama, "parameters": argüman
adlarının listesi}`. Argüman kalıpları modele gitmez; yalnızca adlar.
Sıra sözlüktekiyle aynı.

**Beklenen çıktı:**

```
get_order ['order_id']
order_total ['order_id', 'currency']
```
