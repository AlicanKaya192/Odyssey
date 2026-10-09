`run_order(tasks)` fonksiyonunu yaz: `tasks` `[öncelik, ad]` çiftlerinden
oluşan bir liste. Küçük sayı **daha öncelikli**. Görevlerin **adlarını**
çalışacakları sırayla döndürsün; öncelikleri **eşit** olanlar listedeki
**geliş sırasıyla** çalışsın.

Heap'e `(öncelik, sıra_no, ad)` demetleri koy; `sıra_no` için `enumerate`
yeter. `sorted` ve `sort` yok.

**Beklenen çıktı:**

```
bugfix
deploy
tests
review
docs
```
