## İleri gizlilik nedir

Bir sunucunun uzun ömürlü özel anahtarı yıllar sonra ele geçse ne olur?
Cevap, oturum anahtarlarının nasıl kurulduğuna bağlı.

<figure class="fig">
<div class="versus">
<div class="no">
<h4>Uzun ömürlü anahtarla taşıma</h4>
Her oturumun anahtarı sunucunun kalıcı açık anahtarıyla şifrelenip
gönderilir. O özel anahtar bir gün ele geçerse kaydedilmiş bütün eski
oturumların anahtarları çözülebilir.
</div>
<div class="ok">
<h4>Geçici Diffie-Hellman</h4>
Her oturumda yeni gizli sayılar üretilir, ortak sır hesaplanır ve gizli
sayılar silinir. Uzun ömürlü anahtar yalnızca imza için kullanılır; ele
geçse bile eski oturumların sırrı yeniden hesaplanamaz.
</div>
</div>
<figcaption>İleri gizlilik: bugünün anahtarı çalınsa bile dünün oturumları korunur.</figcaption>
</figure>

## Neden önemli

- Şifreli trafik bugün kaydedilip yıllar sonra çözülmeye çalışılabilir.
- Geçici anahtarlar bu kaydı değersiz kılar: çözmek için gereken gizli
  sayılar artık hiçbir yerde yoktur.
- TLS 1.3'te anahtar değişimi her zaman geçici Diffie-Hellman'la
  (çoğunlukla eğriyle) yapılır; bu yüzden ileri gizlilik zorunludur.

## Kimlik doğrulama ile birlikte

Geçici DH tek başına karşı tarafı doğrulamaz. Doğru düzen:

1. Taraflar geçici açık değerlerini gönderir.
2. Sunucu bu değerleri uzun ömürlü anahtarıyla **imzalar**.
3. İstemci imzayı, sunucunun **sertifikasındaki** açık anahtarla doğrular.
4. Ortak sır HKDF'den geçirilip oturum anahtarları türetilir.

Bu düzenin parçalarını Dijital İmza, Sertifikalar ve PKI ve TLS El
Sıkışması bölümleri tek tek açıyor.
