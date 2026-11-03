Kod incelemesinde (Kod İnceleme ve Statik Analiz bölümü) Top 10'u bir
soru listesine çevirmek işe yarar. Her değişiklik için yalnızca dokunduğu
kategorilerin soruları sorulur. Numaralar 2025 sürümünden.

## Erişim denetimi (A01)

- Bu uç nokta kimin çağırabileceğini denetliyor mu?
- Adresten ya da gövdeden gelen bir numarayla kayıt okunuyorsa, kaydın
  sahibi denetleniyor mu?
- Yetkisiz ile yok aynı cevabı mı veriyor?
- Sunucu kullanıcının verdiği bir adrese istek atıyorsa (SSRF), hedef izin
  listesiyle denetleniyor mu?

## Yapılandırma (A02)

- Yeni bir ayar eklendiyse varsayılanı güvenli mi?
- Hata ayıklama, örnek hesaplar, test uç noktaları yayına gidiyor mu?

## Tedarik zinciri (A03)

- Yeni bir kütüphane eklendiyse gerçekten gerekli mi, bakımı sürüyor mu,
  sürümü sabitlenmiş mi, güvenilir bir kaynaktan mı geliyor?

## Enjeksiyon (A05)

- Kullanıcıdan gelen bir değer SQL, komut ya da HTML metnine
  birleştirilerek mi giriyor? Giriyorsa parametreli sorgu ya da çıktı
  kodlama var mı?

## Tasarım (A06)

- Bu özellik kötüye kullanılırsa ne olur? Sınırsız tekrar edilebilir mi?
- "Bunu kimse denemez" varsayımı var mı?

## Kimlik doğrulama (A07)

- Giriş, parola sıfırlama, MFA akışında hız sınırı var mı?
- Girişte oturum kimliği yenileniyor mu?

## Bütünlük (A08)

- Dışarıdan indirilen ya da gelen bir şey doğrulanmadan çalıştırılıyor ya
  da kullanılıyor mu?

## Kayıt ve uyarı (A09)

- Güvenlikle ilgili olaylar (başarısız giriş, yetki hatası) kaydediliyor
  mu? Önemli olanlar birine haber veriyor mu?
- Kayıtlara parola, jeton, oturum kimliği ya da kişisel veri gidiyor mu?

## Olağandışı durumlar (A10)

- Bir denetimin içinde hata çıkarsa sonuç "izin ver" mi oluyor?
- Her hatayı susturan geniş bir `except` var mı?

## Bir örnek inceleme notu

| Satır | Kategori | Not |
|---|---|---|
| `query = "... WHERE id = " + item_id` | A05 | Parametreli sorguya çevir |
| `return orders[order_id]` | A01 | Sahiplik denetimi yok |
| `log.info(f"login {user} {password}")` | A09 | Parola kayda gidiyor |
| `DEBUG = True` | A02 | Yayında kapalı olmalı |
| `except Exception: return True` | A10 | Hata çıkınca izin veriyor |
