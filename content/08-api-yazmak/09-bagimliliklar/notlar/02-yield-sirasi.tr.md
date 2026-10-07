`yield`'li bir bağımlılıkta neyin hangi sırayla çalıştığı. İki istekle
ölçtük; bağımlılık her adımda bir günlüğe yazıyor:

```python
def resource():
    log.append("open")
    try:
        yield "R"
    except HTTPException as e:
        log.append(f"saw {e.status_code}")
        raise
    finally:
        log.append("close")
```

## Uç nokta başarılı

```text
GET /ok   200 {"r": "R"}
günlük:   open → endpoint → close
```

## Uç nokta `HTTPException` fırlattı

```text
GET /fail   404 {"detail": "nope"}
günlük:     open → endpoint → saw 404 → close
```

- Uç noktanın hatası bağımlılığa **`yield` satırında** geri geliyor;
  `except` onu görebiliyor.
- `finally` her iki durumda da çalıştı.
- `except` içinde `raise` ile hata yeniden fırlatıldı; böylece istemciye
  yine `404` gitti. `raise` yazılmasaydı hata yutulurdu; yapma.

## Ne zaman kullanılır?

| Kaynak | `yield`'den önce | `finally` içinde |
|---|---|---|
| SQLite bağlantısı | `sqlite3.connect(...)` | `conn.close()` |
| İşlem (transaction) | — | hata yoksa `commit`, varsa `rollback` |
| Geçici dosya | dosyayı aç | dosyayı kapat/sil |
| Süre ölçümü | başlangıç zamanı | geçen süreyi yaz |

Veritabanı bölümünde ilk satırı kullanacaksın.
