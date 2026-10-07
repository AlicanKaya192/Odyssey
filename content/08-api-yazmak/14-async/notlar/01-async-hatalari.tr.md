`async` ile en sık yapılan hatalar; hepsi ölçüldü.

## `await` unutmak

```python
async def fetch():
    await asyncio.sleep(0.01)
    return "data"


@app.get("/forgot")
async def forgot():
    result = fetch()            # await yok
    ...
```

`fetch()` çalışmadı; `result` bir **coroutine** nesnesi (`type(result).__name__`
→ `'coroutine'`). Onu cevapta döndürmeye kalkınca `500`. Python ayrıca
"coroutine was never awaited" uyarısı basar. `async def` ile tanımlanan her
şey `await` ile çağrılır.

## `async def` içinde bekleten çağrı

| Bekleten | Neden kötü? | Yerine |
|---|---|---|
| `time.sleep(1)` | Olay döngüsünü kilitler | `await asyncio.sleep(1)` |
| `requests.get(...)` | Aynı | uç noktayı `def` yap |
| `sqlite3` sorgusu | Aynı | uç noktayı `def` yap |
| Büyük bir hesap (milyonlarca döngü) | Aynı | `def` |

Ölçtük: `async def` içinde `time.sleep(0.5)` olan uç noktaya aynı anda beş
istek **2,52 sn** sürdü; doğru yazılanı 0,51 sn.

## `def` içinde `await`

`await` yalnızca `async def` içinde yazılabilir; düz `def` içinde
`SyntaxError`. Düz bir uç noktadan async bir işlevi çağırmak gerekiyorsa uç
noktayı `async def` yap.

## Hangisini seçeyim?

1. İşlevde `await` var mı? → `async def`.
2. Bekleten bir kütüphane (`sqlite3`, `requests`, dosya okuma) var mı? → `def`.
3. İkisi de yok → `def` (güvenli taraf).

Bir projede ikisi karışık olabilir; FastAPI her uç noktaya ayrı karar
veriyor.
