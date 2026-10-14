`two_steps(script, message)` `ChatClient(script)` ile iki adım
çalıştırsın. Birinci adım: hazır `ask` ile `CLASSIFY` talimatını gönder,
cevabı JSON olarak oku; kategori `POLICY`'de yoksa (JSON değilse de)
`[["classify", False], None]` döndür. İkinci adım:
`"Answer using only this policy: " + POLICY[kategori]` talimatıyla aynı
mesajı gönder ve `[["classify", True], cevap]` döndür.

**Beklenen çıktı:**

```
True It arrives in 3 to 5 days.
False None
False None
```
