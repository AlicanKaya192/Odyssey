## Sık yapılan hatalar

| Hata | Neden sorun? | Doğrusu |
|---|---|---|
| Jetonu `random` ile üretmek | Üreteç kriptografik değil, çıktısı tahmin edilebilir | `secrets.token_urlsafe(32)` |
| Tohumu saatten almak | Saat tahmin edilebilir bir değerdir | Tohum hiç verilmez, `secrets` kullanılır |
| Sabit tohum (`random.seed(1)`) | Her çalıştırmada aynı değerler | Yalnızca testte ve benzetimde |
| `bayt % n` | Modulo yanlılığı: bazı sonuçlar daha sık | `secrets.randbelow(n)` |
| Kısa jeton | Az bit, az deneme yeter | En az 128 bit |
| Kendi üretecini yazmak | Rastgele görünür ama incelenmemiştir | İşletim sisteminin kaynağı |
| Aynı nonce'u tekrar kullanmak | Akış şifrelerinde anahtar tekrarı gibi | Her mesaja yeni nonce |

## `random` nerede doğru araç?

- Benzetim ve deney: aynı tohumla sonucu tekrarlayabilmek bir özelliktir.
- Oyun, karıştırılmış soru sırası, örneklem.
- Test verisi üretmek.

Ölçüt tek bir soru: **bu değeri biri tahmin ederse bir zarar doğar mı?**
Cevap evetse `secrets`.

## Kod incelemesinde neye bakılır?

- `import random` olan dosyada `token`, `key`, `salt`, `nonce`, `password`,
  `session`, `reset` gibi adlar.
- `random.seed(...)` çağrısı ve içine verilen değer (özellikle saat).
- `% n` ile aralığa indirilmiş rastgele baytlar.
- Jeton uzunluğu: kaç bayt, kaç bit?
- `random.SystemRandom` güvenlidir (aynı işletim sistemi kaynağını
  kullanır); yalnızca adı yüzünden yanlış alarm verir.

## Savunmayı katmanla

Doğru kaynak tek başına her şeyi çözmez:

- Kısa doğrulama kodlarında (ör. altı hane, yaklaşık 20 bit) deneme sayısı
  sınırlanır ve kod birkaç dakikada geçersiz olur.
- Jeton bir kez kullanılınca silinir.
- Jetonlar karşılaştırılırken süresi sabit karşılaştırma kullanılır
  (`secrets.compare_digest`, Mesaj Doğrulama: HMAC bölümü).
