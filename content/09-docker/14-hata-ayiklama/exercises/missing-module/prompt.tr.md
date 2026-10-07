İmaj kuruluyor ama konteyner hemen düşüyor. `docker logs`:

```text
ModuleNotFoundError: No module named 'helpers'
```

**Yapman gereken:** imajda eksik olan dosyayı da kopyala. (Birden çok
dosyayı tek `COPY`'de vermek için hedef `./` ile bitmeli.)

**Beklenen çıktı:**

```
hi Ada
```
