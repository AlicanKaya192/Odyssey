`log_entry(system, reply)` bir kayıt sözlüğü döndürsün:
`"system_version"`: sistem mesajının UTF-8 baytlarının SHA-256 özetinin
(`hexdigest()`) ilk 8 karakteri; `"reply_words"`: cevabın kelime sayısı
(`reply.split()`).

**Beklenen çıktı:**

```
213c22ed 4
False
```
