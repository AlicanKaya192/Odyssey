Kod incelemesinde (Kod İnceleme ve Statik Analiz bölümü) Top 10'u bir
soru listesine çevirmek işe yarar. Her değişiklik için yalnızca dokunduğu
kategorilerin soruları sorulur.

## Erişim denetimi (A01)

- Bu uç nokta kimin çağırabileceğini denetliyor mu?
- Adresten ya da gövdeden gelen bir numarayla kayıt okunuyorsa, kaydın
  sahibi denetleniyor mu?
- Yetkisiz ile yok aynı cevabı mı veriyor?

## Enjeksiyon (A03)

- Kullanıcıdan gelen bir değer SQL, komut ya da HTML metnine
  birleştirilerek mi giriyor? Giriyorsa parametreli sorgu ya da çıktı
  kodlama var mı?

## Yapılandırma (A05)

- Yeni bir ayar eklendiyse varsayılanı güvenli mi?
- Hata ayıklama, örnek hesaplar, test uç noktaları yayına gidiyor mu?

## Bileşenler (A06)

- Yeni bir kütüphane eklendiyse gerçekten gerekli mi, bakımı sürüyor mu,
  sürümü sabitlenmiş mi?

## Kimlik doğrulama (A07)

- Giriş, parola sıfırlama, MFA akışında hız sınırı var mı?
- Girişte oturum kimliği yenileniyor mu?

## Bütünlük (A08)

- Dışarıdan indirilen ya da gelen bir şey doğrulanmadan çalıştırılıyor ya
  da kullanılıyor mu?

## Kayıt (A09)

- Güvenlikle ilgili olaylar (başarısız giriş, yetki hatası) kaydediliyor
  mu?
- Kayıtlara parola, jeton, oturum kimliği ya da kişisel veri gidiyor mu?

## Tasarım (A04)

- Bu özellik kötüye kullanılırsa ne olur? Sınırsız tekrar edilebilir mi?
- "Bunu kimse denemez" varsayımı var mı?

## Bir örnek inceleme notu

| Satır | Kategori | Not |
|---|---|---|
| `query = "... WHERE id = " + item_id` | A03 | Parametreli sorguya çevir |
| `return orders[order_id]` | A01 | Sahiplik denetimi yok |
| `log.info(f"login {user} {password}")` | A09 | Parola kayda gidiyor |
| `DEBUG = True` | A05 | Yayında kapalı olmalı |
