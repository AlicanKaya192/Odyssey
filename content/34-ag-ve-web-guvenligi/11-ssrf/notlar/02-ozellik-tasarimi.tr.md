SSRF'e karşı en iyi zaman, adres alan bir özelliğin **tasarım**
aşamasıdır.
Aşağıdaki sorular, özellik yazılmadan önce sorulur (Güvensiz Tasarım,
OWASP Top 10 bölümü).

## Tasarım soruları

1. **Kullanıcının adres vermesi gerçekten gerekli mi?** Çoğu zaman
   gerekmez: kullanıcı dosyayı kendisi yükleyebilir ya da bir listeden
   seçebilir. Adres almayan özellikte SSRF olmaz.
2. **Hangi sitelere gidilmesi gerekiyor?** Belli birkaç siteyse izin
   listesi kur. "Her yere" gerekiyorsa iç adres reddi ve ağ sınırlaması
   şart.
3. **Hangi şemalar?** Yalnızca `http` ve `https`.
4. **Hangi portlar?** Genellikle yalnızca 80 ve 443; başka port bir iç
   hizmet olabilir.
5. **Cevapla ne yapılacak?** Yalnızca beklenen tür (resim, belirli bir
   JSON) ve belirli bir boyuta kadar. Ham cevap kullanıcıya gösterilmez.
6. **Hata olursa kullanıcı ne görür?** Genel bir mesaj. "Bağlantı
   reddedildi" ile "zaman aşımı" arasındaki fark bile iç ağda hangi
   adreslerin var olduğunu ele verebilir.

## Uygulama sırası

1. Adresi `urlsplit` ile ayrıştır; şema ve port denetle.
2. Ana bilgisayarı izin listesiyle karşılaştır (varsa).
3. Adı çöz; çıkan **her** IP adresini iç adres kuralıyla denetle.
4. Bağlantıyı denetlenen IP'ye kur; kısa zaman aşımı.
5. Yönlendirmeyi izleme ya da her adımda 1–4'ü tekrarla.
6. Cevabın türünü ve boyutunu denetle.

## Sık hatalar

- `startswith("https://images.example.com")` ile denetlemek.
- Adı denetleyip IP'yi denetlememek.
- Yönlendirmeyi körü körüne izlemek.
- "Bu sunucu zaten içeride, güvenli" diye iç hizmetlerde kimlik
  doğrulamayı kapatmak.
- Hata mesajında iç sunucunun cevabını göstermek.
