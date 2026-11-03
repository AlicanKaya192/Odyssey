`transcript_hash` hazır. `verify_finished(key_hex, messages, tag_hex)`
gelen Finished etiketini doğrulasın: HMAC-SHA256, anahtar `key_hex`,
veri **bütün** mesajların döküm özeti; `hmac.compare_digest` ile
karşılaştır. Başlangıç kodu yalnızca son mesajı özetliyor; ilk mesajdaki
bir değişiklik fark edilmiyor.

**Beklenen çıktı:**

```
True
False
```
