`answer(script, question)` dersteki döngüyü kursun: `ChatClient(script)`
ile `[system, user]` gönder (`tools=SCHEMA`). Cevapta araç çağrısı varsa
`{"role": "assistant", "content": "", "tool_calls": ...}` mesajını ve her
çağrı için hazır `run_tool`'un sonucunu `json.dumps` ile içerik yapan bir
`tool` mesajı ekle, sonra yeniden sor. Döndür: `[son cevabın metni,
mesajların rolleri listesi, çağrı sayısı]`.

**Beklenen çıktı:**

```
Your order is being prepared.
['system', 'user', 'assistant', 'tool']
2
```
