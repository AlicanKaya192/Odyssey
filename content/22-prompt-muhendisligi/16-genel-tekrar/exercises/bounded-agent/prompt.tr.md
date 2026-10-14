`run_agent(script, question, max_rounds)` `ChatClient(script)` ile
`[user]` mesajını `tools=TOOLS` ile göndersin. Cevapta araç çağrısı yoksa
`[metin, tur]` döndürsün. Varsa asistan mesajını (`"content": ""`,
`"tool_calls": ...`) ekleyip her çağrı için `get_order` sonucunu (bilinmeyen
araçta `{"error": "unknown tool"}`) `tool` rolünde `json.dumps` ile
eklesin ve yeniden sorsun. `max_rounds` tur dolarsa `[None, max_rounds]`.

**Beklenen çıktı:**

```
['It shipped on 2026-10-09.', 2]
[None, 3]
```
