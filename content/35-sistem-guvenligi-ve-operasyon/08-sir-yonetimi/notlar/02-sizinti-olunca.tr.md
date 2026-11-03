En dikkatli ekipte bile bir gün bir sır sızar: yanlışlıkla depoya gönderilen
bir yapılandırma dosyası, ekran paylaşımında görünen bir terminal, bir hata
iletisine düşen bir anahtar. Önemli olan sızıntının olmaması kadar,
olduğunda ne yapılacağının önceden bilinmesidir.

## Sızıntı fark edilince

1. **Yenile, sonra temizle.** İlk iş yeni bir değer üretip sistemleri ona
   geçirmek ve eski değeri **iptal etmektir**. Depodan ya da geçmişten
   silmek ikinci iştir; değer zaten kopyalanmış olabilir.
2. **Kapsamı belirle.** Sır neye erişim veriyordu? Hangi sistemler, hangi
   veri? Sızıntı ne zaman oldu, ne zaman fark edildi?
3. **Kullanıldı mı, bak.** Sızıntıdan bu yana o sırla yapılan erişimler
   kayıtlarda aranır (Kayıt ve İzleme bölümü). Beklenmedik bir erişim
   varsa olay müdahalesi başlar (Olay Müdahalesi bölümü).
4. **Kökü düzelt.** Sır neden oraya düştü? Bir `.gitignore` satırı, bir
   ön kayıt (pre-commit) taraması ya da sırrı kasaya taşımak gibi kalıcı
   bir önlem alınır.

## Önlemek için

| Önlem | Neyi yakalar? |
|---|---|
| Ön kayıt sır taraması | Sır depoya girmeden önce |
| Derleme hattında sır taraması | Gözden kaçan sırlar |
| `.gitignore` ile sır dosyalarını dışarıda tutmak | `.env`, anahtar dosyaları |
| Kayıtlarda gizleme | Hata ayıklama satırlarındaki sırlar |
| Kısa ömürlü sırlar | Sızan değerin geçerli kalma süresi |
| En az yetkili sırlar | Sızan sırrın açabileceği kapılar |

## En az yetkili sır

Bir sır, yalnızca işin gerektirdiği yetkiyi vermelidir: raporları okuyan
bir uygulamanın veritabanı kullanıcısı yazamaz; yalnızca bir klasöre
yükleme yapan bir anahtar başka klasörlere dokunamaz. Böylece sızıntı
olduğunda zarar, sırrın açabildiği küçük alanla sınırlı kalır.

## Sırrı paylaşmak

Bir sırrı bir ekip arkadaşına vermek gerektiğinde e-posta, sohbet ya da
belge kullanılmaz: bunlar kopyalanır ve yıllarca saklanır. Doğru yol,
kişiye sır kasasında erişim vermek ya da bir kez açılabilen, süresi dolan
bir paylaşım yöntemi kullanmaktır.
