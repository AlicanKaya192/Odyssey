Model müşterinin mesajından geri arama saatini JSON olarak çıkardı:
`{"date": "YYYY-MM-DD", "time": "HH:MM", "source": "..."}` (`source`
müşterinin kendi sözleri). `check_callback(message, reply, now)` model
cevabını (`reply`, metin) referans an `now`'a (ISO metin) göre denetleyip
şunlardan birini döndürsün, kuralları bu sırayla uygula:

1. JSON okunamıyor, sözlük değil ya da alanlar tam olarak bu üçü değilse
   `"rejected"`.
2. `source` küçük harfle `today at 9am` / `tomorrow at 7pm` biçimine
   (`re.fullmatch`, `am`/`pm` isteğe bağlı) tam uymuyorsa ya da mesajda
   (büyük/küçük harf fark etmeden) geçmiyorsa `"rejected"`.
3. `am`/`pm` yoksa `"needs_clarification"`.
4. Saat 1–12 değilse `"rejected"`.
5. `date` ve `time` referansa göre hesaplananla (`12am` = `00:00`) aynı
   değilse `"rejected"`, aynıysa `"accepted"`.

**Beklenen çıktı:**

```
accepted
needs_clarification
rejected
```
