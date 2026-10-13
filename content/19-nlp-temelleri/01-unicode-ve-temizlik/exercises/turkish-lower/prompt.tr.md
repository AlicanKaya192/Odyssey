`pairs.txt` dosyasının her satırında büyük harfli bir Türkçe kelime ve
doğru küçük hâli var. `turkish_lower(text)` önce `I` harfini `ı`'ya, `İ`
harfini `i`'ye çevirsin, sonra `lower()` uygulasın. Başlangıç kodu düz
`lower()` kullanıyor; bazı satırlar `False` çıkıyor.

Türkçe harfleri klavyeden yazman gerekmiyor: `chr(0x131)` "ı", `chr(0x130)`
"İ".

**Beklenen çıktı:**

```
True
True
True
True
True
True
True
True
```
