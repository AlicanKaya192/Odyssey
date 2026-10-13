"Ã§alÄ±ÅŸma" gibi tuhaf harfler gördüysen metin **yanlış kodlamayla**
okunmuş demektir. Bu bozulmanın adı **mojibake** (Japonca, "karakter
karmaşası").

## Mojibake nasıl oluşur?

```python
text = "çalışma"
data = text.encode("utf-8")
print(data)
print(data.decode("cp1254"))
try:
    "çalışma".encode("cp1254").decode("utf-8")
except UnicodeDecodeError as error:
    print(type(error).__name__, error.reason)
print("çalışma".encode("cp1254").decode("utf-8", errors="replace"))
```

```text
b'\xc3\xa7al\xc4\xb1\xc5\x9fma'
Ã§alÄ±ÅŸma
UnicodeDecodeError invalid continuation byte
�al��ma
```

- "ç" UTF-8'de iki bayt: `\xc3\xa7`. Bu baytlar Türkçe Windows'un eski
  kodlamasıyla (`cp1254`) okununca her bayt ayrı bir harf sanılıyor: "Ã§".
  Dosya bozulmadı; yalnızca yanlış okundu. Doğru kodlamayla yeniden okumak
  yeter.
- Tersi daha gürültülü: `cp1254` ile yazılmış baytları UTF-8 diye okumak
  `UnicodeDecodeError` veriyor, çünkü o baytlar geçerli UTF-8 değil.
- `errors="replace"` okunamayan baytların yerine "�" koyup devam ediyor.
  Programın durmasını önler ama bilgiyi geri getirmez; yalnızca son çare.

**Kural:** dosyayı açarken kodlamayı her zaman açıkça yaz:
`open(yol, encoding="utf-8")`. Yazmazsan Python Windows'ta sistemin eski
kodlamasını kullanabilir ve aynı kod başka bilgisayarda farklı çalışır.

## BOM: dosyanın başındaki görünmez işaret

Windows'un bazı programları UTF-8 dosyanın başına üç baytlık bir işaret
(byte order mark, BOM) koyar.

```python
from pathlib import Path

Path("notes.txt").write_text("hello", encoding="utf-8-sig")
print(Path("notes.txt").read_bytes())
first = Path("notes.txt").read_text(encoding="utf-8")
print(ascii(first), first == "hello")
print(Path("notes.txt").read_text(encoding="utf-8-sig") == "hello")
```

```text
b'\xef\xbb\xbfhello'
'\ufeffhello' False
True
```

`utf-8` ile okununca BOM metnin başında `\ufeff` olarak kalıyor ve ilk
kelime ("hello") hiçbir şeyle eşleşmiyor. CSV dosyasında ilk sütunun adı
bozuk görünür. Çözüm: `encoding="utf-8-sig"` ile okumak; BOM varsa atar,
yoksa düz UTF-8 gibi okur.

## Kısa teşhis listesi

| Gördüğün | Sebep | Çözüm |
|---|---|---|
| `Ã§`, `Ä±`, `ÅŸ` | UTF-8 dosya eski kodlamayla okunmuş | `encoding="utf-8"` |
| `UnicodeDecodeError` | Eski kodlamalı dosya UTF-8 sanılmış | Doğru kodlamayı bul (`cp1254`, `latin-1`) |
| İlk kelime eşleşmiyor | BOM | `encoding="utf-8-sig"` |
| "�" işaretleri | Daha önce `errors="replace"` ile okunmuş | Kaynağa dönüp doğru oku |
