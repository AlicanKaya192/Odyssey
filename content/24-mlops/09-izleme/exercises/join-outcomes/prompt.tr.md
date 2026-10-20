Tahmin kaydı bir liste (`{"id": ..., "churn_probability": ...}`), gerçek sonuçlar sonradan gelen bir sözlük (`{kimlik: 0 ya da 1}`). `join_outcomes(log, outcomes, threshold)` fonksiyonunu yaz ve `[doğru, toplam]` döndür:

- Sonucu henüz gelmemiş kayıtları atla.
- Olasılık `threshold` ya da üstündeyse tahmin `1`, değilse `0`.
- Tahmin gerçek sonuçla aynıysa doğru say.

**Beklenen çıktı:**

```
[2, 3]
```
