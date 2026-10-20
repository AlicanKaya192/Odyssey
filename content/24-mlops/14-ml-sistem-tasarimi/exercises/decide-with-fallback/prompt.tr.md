Model çökünce yedek kurala geçen `decide(score, threshold, customer)` fonksiyonunu yaz:

- `score` `None` ise model çalışmadı: müşterinin `"support_calls"` değeri en az `2` ise teklif et.
- Değilse `score` en az `threshold` ise teklif et.
- Teklifse `"offer"`, değilse `"no offer"` döndür.

**Beklenen çıktı:**

```
offer
no offer
offer
no offer
```
