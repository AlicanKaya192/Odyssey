Bazı dillerde birden çok kelimeden oluşan değişken adları **camel case** (deve hörgücü) ile yazılır: ilk kelimenin ilk harfi küçük, sonraki her kelimenin ilk harfi büyük: `name`, `firstName`, `preferredFirstName`. Python ise **snake case**'i (yılan) önerir: kelimeler alt çizgiyle ayrılır, bütün harfler küçük: `name`, `first_name`, `preferred_first_name`.

Kullanıcıdan camel case bir değişken adı isteyen ve snake case karşılığını yazan bir program yaz. Girdinin gerçekten camel case olduğunu varsayabilirsin. (CS50'de dosyanın adı `camel.py`.)

İpucu (CS50'den): bir dizeyi `for c in s:` ile harf harf gezebilirsin; `c.isupper()` harf büyükse `True`.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `name` → çıktı `name`
- Girdi `firstName` → çıktı `first_name`
- Girdi `preferredFirstName` → çıktı `preferred_first_name`
- Girdi `isHttpRequestOk` → çıktı `is_http_request_ok`
