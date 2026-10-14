Bir LLM çağrısında karşılaşılan durumlar ve ne yapılacağı:

| Durum | Yeniden dene? | Ne yapılır? |
|---|---|---|
| İstek sınırı (429) | Evet | Üstel bekleme + jitter; servis süre söylüyorsa ona uy |
| Servis hatası (5xx) | Evet | Üstel bekleme + jitter, deneme sınırı |
| Zaman aşımı | Dikkatli | Okuma isteğiyse evet; değiştiren istekse yalnızca istek kimliğiyle |
| Pencereye sığmama | Hayır | Geçmişi kırp, belgeyi parçala, `max_tokens`'ı küçült |
| Bozuk istek (rol, içerik) | Hayır | Kodu düzelt; bu bir program hatası |
| Kimlik bilgisi yanlış | Hayır | Ayarı düzelt; tekrar göndermek hiçbir şey değiştirmez |
| `finish_reason == "length"` | Bir kez, daha büyük sınırla | `max_tokens`'ı beklenen cevaba göre seç; prompt yeniden ödenir |
| Bütün denemeler bitti | — | Yedek cevap + kayıt; program çökmez |

**Yeniden deneme iskeleti:**

```python
for attempt in range(attempts):
    try:
        return client.chat(messages, max_tokens=max_tokens)
    except (RateLimitError, ServerError):
        wait = random.uniform(0, base * 2 ** attempt)
        if attempt == attempts - 1 or waited + wait > deadline:
            return FALLBACK
        sleep(wait)
        waited += wait
```

**Sık hatalar:**

- **Her hatayı yeniden denemek.** Kalıcı hata her denemede aynı gelir;
  yalnızca kullanıcıyı bekletir.
- **Sınırsız deneme.** Servis uzun süre kapalıysa program hiç cevap
  vermez.
- **Sabit bekleme.** Aynı anda hata alan istemciler aynı anda geri gelir.
- **Değiştiren isteği kimliksiz yeniden denemek.** İş iki kez yapılabilir.
- **Önbellek anahtarına cevabı etkileyen bir şeyi koymamak.** Sistem
  mesajı ya da ayar değişince eski cevap dönmeye devam eder.
