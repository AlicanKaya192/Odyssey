## Dört kip

| Kip | Nasıl çalışır | Aynı blok → aynı çıktı | Dolgu | Durum |
|---|---|---|---|---|
| ECB | Her blok ayrı şifrelenir | Evet | İster | **Kullanılmaz** |
| CBC | Blok, önceki şifreli blokla XOR'lanıp şifrelenir | Hayır | İster | Eski sistemlerde |
| CTR | Nonce + sayaç şifrelenir, mesajla XOR'lanır | Hayır | İstemez | Bütünlükle birlikte |
| GCM | CTR + doğrulama etiketi | Hayır | İstemez | **Önerilen** |

## ECB neden sızdırır

- Aynı anahtar, aynı düz metin bloğu → aynı şifreli blok.
- Tekrar eden veri (aynı başlık, aynı alan, bir resmin düz renkli bölgeleri)
  şifreli metinde de tekrar eder.
- Anahtar güçlü olsa bile kalıp görünür; sorun şifrede değil kiptedir.

## CBC

- İlk blok IV ile, sonraki her blok bir önceki şifreli blokla XOR'lanır.
- Çözerken sıra tersine: blok çözülür, sonra önceki şifreli blokla XOR'lanır.
- IV rastgele ve tahmin edilemez olmalı; şifreli metnin başında gönderilir.

## CTR

- Şifrelenen şey düz metin değil `nonce + sayaç`; çıkan anahtar dizisidir.
- Şifreleme ve çözme aynı işlem; blok çözme işlevi hiç gerekmez.
- Bloklar birbirinden bağımsız, paralel işlenebilir.
- Nonce aynı anahtarla tekrarlanırsa tek kullanımlık şifrenin tekrar-anahtar
  hatasına düşer.

## Ortak eksik

ECB, CBC ve CTR yalnızca **gizlilik** verir. Şifreli metindeki bir bit
değiştirilirse alıcı bunu fark etmez. Bütünlük için doğrulanmış kip (GCM)
ya da şifreleme + MAC gerekir.
