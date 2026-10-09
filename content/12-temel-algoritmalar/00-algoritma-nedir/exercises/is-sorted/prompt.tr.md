`is_sorted(numbers)` fonksiyonunu yaz: liste küçükten büyüğe sıralıysa
`True`, değilse `False` döndürsün. Eşit komşular sıralı sayılır
(`[1, 2, 2, 3]` sıralı).

**Kurallar:**

- `sorted()` ve `.sort()` kullanma.
- Boş liste ve tek elemanlı liste sıralı sayılır.

**İpucu fikri:** Bir liste sıralıysa her eleman **sağındaki komşusundan
büyük olamaz**. Tek bir ihlal görmek `False` demeye yeter; hemen dönebilirsin.

**Beklenen çıktı:**

```
True
False
True
```
