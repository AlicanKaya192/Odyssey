TLS bağlantıyı korur; ama neyi korumadığını bilmek de önemli.

| TLS korur | TLS korumaz |
|---|---|
| Yoldaki verinin gizliliği ve bütünlüğü | Sunucuya ulaştıktan sonra verinin nasıl saklandığı |
| Bağlanılan sunucunun o ada ait olduğu | Sitenin kendisinin güvenilir olduğu (sahte site de sertifika alabilir) |
| Değiştirilmiş el sıkışmanın yakalanması | Uygulamadaki açıklar (SQL enjeksiyonu, yetki hataları) |
| Eski oturumların ileri gizliliği | Uç noktadaki zararlı yazılım |

## Açıkta kalan bilgiler

- Bağlanılan **alan adı** el sıkışmanın başında çoğunlukla açıktır
  (SNI alanı); yalnızca içerik şifrelidir.
- Trafiğin **miktarı ve zamanlaması** görülebilir.
- IP adresleri her zaman görünür.

## 0-RTT

TLS 1.3, daha önce bağlanılmış bir sunucuya ilk mesajla birlikte veri
göndermeye (0-RTT) izin verir. Hızlıdır ama o ilk veri **yeniden
oynatılabilir**: aynı istek iki kez işlenebilir. Bu yüzden 0-RTT yalnızca
tekrar edilmesi zararsız istekler (bir sayfayı okumak gibi) için kullanılır,
para gönderme gibi işlemler için değil.

## "Kilit simgesi" ne demek

Tarayıcıdaki kilit, bağlantının şifreli olduğunu ve sertifikanın o alan
adına verildiğini söyler. Sitenin dürüst olduğunu söylemez: Sosyal
Mühendislik bölümündeki benzer alan adlı sahte siteler de geçerli bir
sertifika alabilir. Önemli olan alan adının kendisidir.
