## Şifreler tek satırda

| Şifre | Tür | Anahtar | Anahtar sayısı | Neden kırılır? |
|---|---|---|---|---|
| Sezar | Yer değiştirme | Kaydırma | 26 | Kaba kuvvet |
| ROT13 | Yer değiştirme | Yok (13) | 1 | Anahtarı yok |
| Atbash | Yer değiştirme | Yok | 1 | Anahtarı yok |
| Yerine koyma | Yer değiştirme | 26 harfin sırası | 26! ≈ 2⁸⁸ | Harf sıklığı |
| Vigenère | Çok alfabeli yer değiştirme | Anahtar kelime | 26ᵏ | Anahtar tekrar eder |
| Çit şifresi | Yer karıştırma | Satır sayısı | Az | Sıklık aynı kalır |

## Python kalıpları

- Harfin alfabe sırası: `ord(ch) - ord("a")`.
- Geri harfe: `chr(sira % 26 + ord("a"))`.
- Büyük-küçük harfi korumak: `base = ord("A") if ch.isupper() else ord("a")`.
- Harf olmayanı olduğu gibi bırak: `if ch.isalpha() and ch.isascii():`.
- Tablo ile yerine koyma: `str.maketrans(duz, anahtar)` ve `metin.translate(tablo)`.
- Vigenère'de anahtarın sırası yalnızca harflerde ilerler.

## Akılda tutulacak

- Çözmek = ters yönde kaydırmak (`-shift`).
- Büyük anahtar uzayı tek başına güvenlik değildir.
- Yer değiştirme → karışıklık (confusion), yer karıştırma → yayılma
  (diffusion).
