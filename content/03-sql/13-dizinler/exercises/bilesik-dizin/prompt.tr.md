Bu sorgu için **iki sütunlu tek bir dizin** kur:

```sql
SELECT id FROM events
WHERE customer_id = 3
  AND created_at >= '2025-06-01' AND created_at < '2025-06-02';
```

Sütunların sırası önemli. Eşitlikle aranan sütun (`customer_id`) önde,
aralıkla aranan (`created_at`) arkada olsun.

Neden bu sıra, ölçüldü:

| Sorgu | `(customer_id, created_at)` | `(created_at, customer_id)` |
|---|---|---|
| müşteri 3, bir gün | 2 okuma | 2 okuma |
| yalnız müşteri 3 | **11 okuma** | 52 okuma (tarama) |

Bu sorgu için ikisi de yetiyor, ama `customer_id` önde olan dizin
"müşterinin bütün olayları" sorgusunu da taşıyor; ters sıradaki taşımıyor.
Dizin yalnızca **ilk sütunu** bilinen aramalarda doğrudan yere gidebiliyor.

Denetim dizinin anahtar sütunlarına ve sırasına bakıyor; iki ayrı dizin
geçmiyor.
