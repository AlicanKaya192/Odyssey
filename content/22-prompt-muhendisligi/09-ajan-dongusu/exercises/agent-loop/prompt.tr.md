`agent(script, question, max_steps)` dersteki döngüyü kursun:
`ChatClient(script)`; her turda `tools=SCHEMA` ile sor, `input_tokens`'ı
ize ekle. Araç çağrısı yoksa `[cevap, tur, iz]` döndür. Varsa `assistant`
mesajını ekle; her çağrı için aynı çağrı (`json.dumps(call,
sort_keys=True)`) daha önce geldiyse `{"error": "you already made this
call"}`, gelmediyse hazır `run_tool` sonucu bir `tool` mesajı olarak
eklensin. `max_steps` tur dolarsa `[None, max_steps, iz]`.

**Beklenen çıktı:**

```
It is being prepared. 2
[37, 57]
None 3
[37, 57, 80]
```
