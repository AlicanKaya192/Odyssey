`fit_chunks(chunks, budget)` sıralanmış parça listesini baştan gezsin ve
`count_tokens` (salt okunur `llm_client.py`) ile toplamı `budget`'ı aşmayan
parçaları alsın; aşacak ilk parçada dursun. Döndür: `[alınan parça sayısı,
toplam token]`.

**Beklenen çıktı:**

```
[1, 11]
[3, 28]
```
