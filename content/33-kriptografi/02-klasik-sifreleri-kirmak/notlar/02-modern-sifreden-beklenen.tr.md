Bu bölümdeki saldırıların hepsi aynı şeyi kullandı: şifreli metin düz
metin hakkında bir şey söylüyordu. Modern bir şifreden beklenenler bu
yüzden şöyle sıralanır.

## 1. Rastgeleden ayırt edilemez çıktı

Anahtarı bilmeyen biri şifreli metne bakıp onun bir şifre mi yoksa
rastgele baytlar mı olduğunu söyleyemesin. Harf sıklığı, tesadüf indeksi,
tekrar eden parçalar: hiçbiri bir iz bırakmasın.

## 2. Yayılma: bir bit, her şey

Düz metinde tek bir bit değişince şifreli metnin yaklaşık yarısı
değişsin. Klasik şifrelerde bir harf değişince yalnızca bir harf
değişiyordu; bu, saldırgana hangi parçanın neye karşılık geldiğini
öğretiyordu. (Kriptografi Nedir? bölümünde aynı etkiyi özet fonksiyonunda
gördük.)

## 3. Bilinen düz metne dayanıklılık

Saldırgan bazı düz metin–şifreli metin çiftlerini bilse bile (bir e-postanın
"Merhaba" ile başladığını bilmek gibi) anahtarı ya da öteki mesajları
öğrenemesin. Gerçek hayatta saldırgan neredeyse her zaman bir şeyler bilir.

## 4. Aynı mesaj, farklı şifreli metin

Aynı mesaj iki kez şifrelenince aynı şifreli metin çıkmasın; yoksa
saldırgan "bu iki mesaj aynı" bilgisini edinir. Bunu sağlayan başlangıç
değeri (IV, nonce) Blok Şifre Kipleri ve IV bölümünde.

## 5. Güvenlik yalnızca anahtarda

Algoritma herkesçe bilinsin (Kerckhoffs) ve anahtar uzayı kaba kuvveti
imkânsız kılacak kadar büyük olsun (128 bit ve üstü).

## Klasik şifreler bu listede nerede düşer?

| Beklenti | Sezar | Yerine koyma | Vigenère |
|---|---|---|---|
| Rastgeleden ayırt edilemez | Hayır | Hayır | Hayır (IoC) |
| Yayılma | Hayır | Hayır | Hayır |
| Bilinen düz metin | Tek harf yeter | Birkaç harf yeter | Anahtar uzunluğu kadar harf yeter |
| Aynı mesaj, farklı çıktı | Hayır | Hayır | Hayır |
| Büyük anahtar uzayı | Hayır (26) | Evet (2⁸⁸) | Anahtar uzunluğuna bağlı |
