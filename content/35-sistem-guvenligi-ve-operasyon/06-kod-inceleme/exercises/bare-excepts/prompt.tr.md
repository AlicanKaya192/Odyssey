`bare_excepts(source)` türü yazılmamış her `except:` bloğunun satır
numarasını küçükten büyüğe bir liste olarak döndürsün. Türü olan
yakalamalar (`except FileNotFoundError:`) sayılmaz. AST'de türsüz
yakalama, `type` alanı `None` olan bir `ast.ExceptHandler`'dır.

**Beklenen çıktı:**

```
[4, 12]
```
