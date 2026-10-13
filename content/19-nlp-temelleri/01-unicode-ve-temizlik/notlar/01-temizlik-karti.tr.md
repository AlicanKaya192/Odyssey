Metin temizlerken en sık kullanılan araçlar.

## Fonksiyonlar

| Araç | Ne yapar | Örnek |
|---|---|---|
| `ord(c)` / `chr(n)` | Karakter ↔ kod noktası | `ord("ş")` → 351 |
| `s.encode("utf-8")` / `b.decode("utf-8")` | Metin ↔ bayt | `"ş".encode()` → `b'\xc5\x9f'` |
| `unicodedata.normalize("NFC", s)` | Harf + işareti birleştirir | iki "café" eşitlenir |
| `unicodedata.normalize("NFD", s)` | Harf ile işareti ayırır | aksan atmanın ilk adımı |
| `unicodedata.normalize("NFKC", s)` | Görsel çeşitleri sadeleştirir | "ＡＢＣ" → "ABC", "…" → "..." |
| `unicodedata.combining(c)` | Birleşen işaret mi? | aksanları süzmek |
| `unicodedata.name(c)` | Karakterin resmî adı | görünmeyeni avlamak |
| `html.unescape(s)` | HTML varlıklarını çözer | `&amp;` → `&` |
| `re.sub(r"<[^>]+>", " ", s)` | HTML etiketlerini siler | `<br>` → boşluk |
| `str.maketrans` + `translate` | Harf harf eşleme | Türkçe `lower` |
| `" ".join(s.split())` | Her boşluğu tek boşluk yapar | sekme, `\xa0`, satır sonu |
| `ascii(s)` | Görünmeyenleri kod olarak yazar | `'a\xa0b'` |

## Görünmeyen ve benzeyen karakterler

| Karakter | Kod | Nereden gelir | Sorun |
|---|---|---|---|
| Bölünmez boşluk | U+00A0 | Web, kelime işlemci | `split(" ")` bölmez |
| Sıfır genişlikli boşluk | U+200B | Web editörleri | Görünmez, kelimeye yapışır |
| BOM | U+FEFF | Windows Not Defteri | Dosyanın ilk satırını bozar |
| Yumuşak tire | U+00AD | Kopyalanan metin | Görünmez, kelimeyi böler |
| Kıvrık tırnak | U+2018, U+2019, U+201C, U+201D | Kelime işlemci | `'` ile eşleşmez |
| Uzun tire | U+2013, U+2014 | Kelime işlemci | `-` ile eşleşmez |

`str.split()` argümansız çağrılınca bölünmez boşluğu da boşluk sayar, ama
sıfır genişlikli boşluk, BOM ve yumuşak tire "boşluk" değil: onları elle
silmek gerekir.

## Önerilen sıra

1. Doğru kodlamayla oku (`encoding="utf-8"`, BOM varsa `"utf-8-sig"`).
2. HTML varlıklarını çöz, etiketleri sil.
3. Normalleştir (NFC; görsel çeşitler de gidecekse NFKC).
4. Tırnakları ve tireleri düzle, görünmez karakterleri sil.
5. Boşlukları teke indir.
6. Göreve göre: küçük harf (Türkçede `translate` ile), aksan, noktalama.

İlk beş adım hemen her görevde zararsız. Altıncı adım bilgi götürebilir; her
seferinde görevine bakarak karar ver.
