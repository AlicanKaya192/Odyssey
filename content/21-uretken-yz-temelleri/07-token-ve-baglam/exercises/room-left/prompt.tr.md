`room(messages, window)` salt okunur `llm_client.py`'deki
`count_message_tokens` ile mesaj listesinin token sayısını bulsun ve
`[giren token, cevap için kalan en fazla token]` döndürsün. Kalan yer
`window - giren`, ama 0'ın altına düşmez.

**Beklenen çıktı:**

```
[14, 86]
[14, 0]
```
