`embed_batch(batch_ids, vocab_size, dim)` `padding_idx=0` olan bir
`nn.Embedding(vocab_size, dim)` kursun (tohum başlangıçta hazır) ve dolgulu
grubu ondan geçirsin. Üç öğeli bir liste döndürsün: çıkışın şekli (liste),
vektörü tamamen sıfır olan konum sayısı ve katmanın parametre sayısı.

**Beklenen çıktı:**

```
[[2, 4, 4], 3, 40]
```
