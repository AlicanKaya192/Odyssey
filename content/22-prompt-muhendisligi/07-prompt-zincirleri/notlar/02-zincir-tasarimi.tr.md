Bir zinciri kurarken her adım için şu tabloyu doldur:

| Adım | Girdi | Çıktı | Doğrulama | Düşerse |
|---|---|---|---|---|
| Sınıflandır | Müşteri mesajı | `{"category": ...}` | Kategori listede mi? | Yeniden sor, sonra insana |
| Çıkar | Müşteri mesajı | `{"order_id": ...}` | Alan var mı, kalıba uyuyor mu? | `null` say ya da yeniden sor |
| Cevap yaz | Mesaj + ilgili kural | Düz metin | Cevap kuralları (uzunluk, vaat yok) | Kısalt ya da insana |

**Tasarım soruları:**

1. Bu iş gerçekten birbirinden farklı alt işlerden mi oluşuyor?
2. Bir adımın hatası sonrakileri bozuyor mu? Bozuyorsa o adımı ayrı
   denetle.
3. Her adım hangi bağlamı gerektiriyor? Gerekmeyeni gönderme.
4. Hangi adımlar her mesajda gerekmiyor? Koşulla atla.
5. Zincirin toplam token'ı ve çağrı sayısı tek prompt'tan fazla mı?
   Ölç.

**Kayıt:**

- Her adım için ad, başarı, giren ve çıkan token, süre.
- Zincir durduysa durduğu adım ve sebebi.
- Kullanılan şablonların adı ve sürümü.

**Sık hatalar:**

- **Bir adımın çıktısını doğrulamadan sonrakine vermek.** Hata
  zincir boyunca büyür.
- **Basit bir işi zincire bölmek.** Yalnızca çağrı ve gecikme artar.
- **Her adıma bütün bağlamı göndermek.** Zincirin bağlam seçme faydası
  kaybolur.
- **Durmanın sebebini kaydetmemek.** Hangi adımın iyileştirileceği
  bilinmez.
