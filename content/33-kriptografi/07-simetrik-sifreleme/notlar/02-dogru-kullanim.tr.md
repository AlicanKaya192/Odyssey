Simetrik şifrelemeyi doğru kullanmak, algoritmayı seçmekten çok onu nasıl
kullandığına bağlıdır. Bu bölümdeki ve önceki bölümlerdeki dersleri bir
araya getiren kontrol listesi:

## Anahtar

- En az 128 bit, gerçekten rastgele (`secrets`/`os.urandom`; `random`
  değil).
- Koda yazılmaz; yapılandırmadan ya da sır kasasından okunur.
- Şifreleme anahtarıyla MAC anahtarı ayrıdır; tek bir ana sırdan ayrı
  türetilir (Anahtar Türetme bölümü).
- Parolayı doğrudan anahtar olarak kullanma; paroladan anahtar bir KDF ile
  türetilir.

## Nonce / IV

- Her mesajda benzersiz. En güvenli yol rastgele üretmek ya da güvenli bir
  sayaç tutmak.
- Aynı anahtarla asla tekrarlanmaz.
- Gizli değildir; şifreli metnin yanında saklanır/gönderilir.

## Gizlilik yetmez: bütünlük de gerekir

- Tek başına şifreleme mesajın değiştirilmesini engellemez (XOR bölümündeki
  bit çevirme).
- Çözüm: şifreleme + MAC ya da ikisini birlikte yapan **doğrulanmış
  şifreleme** (AES-GCM, ChaCha20-Poly1305). Doğrulanmış Şifreleme bölümü.
- Alıcı **önce** etiketi doğrular, sonra çözer.

## Kütüphane kullan

- AES ve modern akış şifreleri standart kütüphanede yoktur; denenmiş bir
  kütüphanenin yüksek düzeyli, doğrulanmış işlevi kullanılır.
- Kipleri, dolguyu ve nonce'u elle birleştirmek yerine tek bir
  "şifrele/çöz" çağrısı tercih edilir; ayrıntı ne kadar azsa hata o kadar
  az.
- Bu notta ve derste yazdığımız her şey **öğrenmek** içindir, üretimde
  kullanmak için değil.
