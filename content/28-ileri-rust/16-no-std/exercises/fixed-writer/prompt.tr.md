`Buffer` için `core::fmt::Write` yaz, sığmayan metinde `Err(fmt::Error)` döndür. `report`: `ad=değer` biçimini `write!` ile yazsın.

**Beklenen çıktı:**

```text
Ok(())
a=5
Err(Error)
true
```
