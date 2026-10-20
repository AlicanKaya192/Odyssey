Bir modeli yalnızca eğitimde kullanılan sütunlar ilgilendirir. Müşteri kimliği (`id`) değişse de model aynı veriyle eğitilmiş olur.

`fingerprint(rows, columns)` fonksiyonunu yaz:

- Her satırdan yalnızca `columns` listesindeki anahtarları tut.
- Sonucu `json.dumps(..., sort_keys=True)` ile metne çevir.
- Metnin SHA-256 özetinin onaltılık yazımının **ilk 12** karakterini döndür.

Anahtarların sırası farklı olsa da aynı veri aynı parmak izini vermeli.

**Beklenen çıktı:**

```
features: 3f27fa9366f6
new ids: 3f27fa9366f6
one change: 945c38617509
```
