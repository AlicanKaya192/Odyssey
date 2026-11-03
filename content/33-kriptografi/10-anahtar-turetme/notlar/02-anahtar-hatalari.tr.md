Anahtar türetmede yapılan hataların çoğu "çalışıyor" görünür; şifreleme
de çözme de olur. Sorun ancak biri parolayı tahmin etmeye çalıştığında ya
da iki anahtarın aynı çıktığı fark edildiğinde ortaya çıkar.

| Hata | Neden sorun | Doğrusu |
|---|---|---|
| Parolayı doğrudan anahtar yapmak | Uzunluk tutmaz, rastgele değil | PBKDF2 / scrypt / Argon2id |
| Parolayı tek `sha256` ile anahtara çevirmek | Tahmin denemesi çok hızlı | Yavaş, tuzlu KDF |
| Tuz kullanmamak ya da herkese aynı tuz | Aynı parola aynı anahtar verir | Kayıt başına rastgele tuz |
| Tuzu gizli sanıp saklamamak | Anahtar yeniden türetilemez, veri kaybolur | Tuz verinin yanında açıkça saklanır |
| Tekrar sayısını küçük tutmak | Yavaşlık kalmaz | Güncel öneriye göre; zamanla artırılır |
| Parametreleri kayda yazmamak | Sonradan tekrar sayısı artırılamaz | KDF adı ve parametreleri kayıtta |
| Şifreleme ve MAC için aynı türetilmiş anahtar | İki işlem birbirini zayıflatabilir | HKDF, farklı `info` etiketleri |
| HKDF'ye doğrudan parola vermek | HKDF hızlıdır, tahmini yavaşlatmaz | Önce yavaş KDF, sonra HKDF |
| Türetilmiş anahtarı diske yazmak | Parolanın koruması boşa gider | Anahtar her seferinde yeniden türetilir |

## Tekrar sayısını yükseltmek

Kayıtta tekrar sayısı yazılıysa, kullanıcı bir sonraki girişinde doğru
parolayı verdiğinde anahtar (ya da parola özeti) yeni, daha yüksek sayıyla
yeniden hesaplanıp kaydedilebilir. Parametresi yazılmamış kayıtta bu
mümkün değildir. Parolaları Saklamak bölümündeki kayıt biçimi
(`algoritma$tekrar$tuz$özet`) bu yüzden parametreyi de taşır.
