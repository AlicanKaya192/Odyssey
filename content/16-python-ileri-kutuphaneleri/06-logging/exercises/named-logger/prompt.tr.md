`get_logger(name)` fonksiyonunu yaz: `"shop."` ön ekli adla bir kaydedici
döndürsün (`logging.getLogger(f"shop.{name}")`). Aynı adla iki çağrı aynı
nesneyi vermeli.

**Beklenen çıktı:**

```
shop.db True 30
```
