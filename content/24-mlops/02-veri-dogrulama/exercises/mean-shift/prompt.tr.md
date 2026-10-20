`mean_shift(reference, rows, column)` fonksiyonunu yaz. Yeni partinin bir sütunundaki ortalamanın, referans veriye göre kaç **standart sapma** kaydığını ölç:

- İki listede de `None` olan değerleri atla.
- `|yeni ortalama - referans ortalaması| / referans standart sapması`.
- Ortalama için `statistics.mean`, standart sapma için `statistics.pstdev` kullan.
- Sonucu iki basamağa yuvarla.

Kod 3. ayın müşterilerini 0. ayınkilerle karşılaştırıyor; müşteriler aylar geçtikçe değişiyor.

**Beklenen çıktı:**

```
tenure 0.03 ok
monthly_fee 0.27 ok
support_calls 0.53 CHECK
usage_hours 0.54 CHECK
```
