`assistant(script, message)` dersteki yolu kursun (yeniden deneme yok).
Mesaj `DETECT`'e uyarsa `["blocked", ""]`. Yoksa `ChatClient(script)` ile
sınıflandır (`[system "Answer with one category word.", user]`,
`max_tokens=20`, `parse_label`). Kategori yoksa ya da `TO_PEOPLE`'daysa
`["handover", ""]`. Sipariş verisini `get_order` ile bul, `SYSTEM` ve
`f"Order data: {data}\n\nCustomer: {message}"` ile cevap iste
(`max_tokens=80`; veri yoksa `data` `"none"`). Hazır `problems` doğruysa
`["handover", cevap]`, değilse `["sent", cevap]`.

**Beklenen çıktı:**

```
sent
blocked
handover
handover
```
