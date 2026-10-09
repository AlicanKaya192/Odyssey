`transaction(data)` bağlam yöneticisini `@contextmanager` ile yaz: girerken
sözlüğün kopyasını alsın, `data`'yı versin (`yield data`). Blokta hata çıkarsa
sözlüğü kopyasına geri döndürsün (`clear` + `update`) ve hatayı **yeniden
fırlatsın** (`raise`).

**Beklenen çıktı:**

```
{'balance': 70}
ValueError: not enough money
{'balance': 70}
```
