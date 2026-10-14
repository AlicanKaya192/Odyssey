`finish(proposed, max_tokens)` modelin sırayla üreteceği token'ları
(`proposed`) alsın ve üretim döngüsünü taklit etsin: `"<end>"` gelirse dur ve
`[metin, "stop"]` döndür; üretilen token sayısı `max_tokens`'a ulaşırsa
`[metin, "length"]` döndür. Metin, üretilen token'ların boşlukla
birleşimi (`"<end>"` metne girmez).

**Beklenen çıktı:**

```
['paris .', 'stop']
['the capital of', 'length']
```
