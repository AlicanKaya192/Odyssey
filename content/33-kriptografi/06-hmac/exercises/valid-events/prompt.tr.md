`make_tag` hazır. `events` her biri `[body, tag]` olan bir liste; hepsi
aynı `key_hex` ile doğrulanacak. `valid_events(key_hex, events)` etiketi
**geçerli** olan gövdeleri döndürsün: abece sıralı ve tekrarsız.
Karşılaştırma `hmac.compare_digest` ile.

**Beklenen çıktı:**

```
order 1
order 2
```
