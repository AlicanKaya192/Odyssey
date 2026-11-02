Sosyal Mühendislik bölümünü uygula. Her e-posta `id`, `from` ve
isteğe bağlı `links`, `urgent`, `asks_password` alanlı. `belongs` hazır.

`triage_mail(mails, domain, threshold)` her e-postaya puan versin:

- gönderenin `@`'den sonraki alan adı `domain`'e ait değilse +3,
- bağlantılardan en az birinin sunucusu (`urlsplit(url).hostname`)
  `domain`'e ait değilse +2 (bir kez),
- `urgent` ise +2, `asks_password` ise +3.

Puanı `threshold`'a eşit ya da büyük olanları `[id, puan]` olarak, puan
büyükten küçüğe, eşitlikte `id` sırasında döndürsün.

**Beklenen çıktı:**

```
m2 10
m4 5
```
