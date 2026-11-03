## Güvenlik inceleme listesi

| Konu | Sorulacak soru |
|---|---|
| Girdi | Dışarıdan gelen her veri izin listesiyle doğrulanıyor mu? |
| Çıktı | Veri HTML'e, SQL'e, komuta giderken kodlanıyor ya da parametreleniyor mu? |
| Kimlik | Uç nokta giriş istiyor mu? |
| Yetki | Sahiplik ve rol her istekte sunucuda denetleniyor mu? |
| Hata | Hata olunca denetim reddediyor mu; hata iletisi iç bilgi sızdırıyor mu? |
| Sırlar | Kodda, yapılandırmada ya da kayıtta parola, anahtar, jeton var mı? |
| Kripto | Kendi şifreleme yok; güvenilir kütüphane, doğru kip |
| Bağımlılık | Yeni paket gerekli mi, sürümü sabit mi? |
| Silinenler | Değişiklik bir denetimi, testi ya da kaydı kaldırıyor mu? |

## İyi inceleme alışkanlıkları

- Küçük değişiklik iste: bin satırlık fark gerçekten okunmaz.
- Önce silinen satırları oku.
- "Bu neden güvenli?" diye sor; cevap kodda ya da açıklamada olmalı.
- Bulguyu kişiye değil koda yaz; amaç suçlu bulmak değil hatayı.

## AST kalıpları

| Aranan | Düğüm |
|---|---|
| Fonksiyon çağrısı | `ast.Call`, adı `node.func.id` |
| Metot çağrısı | `ast.Call`, `node.func` bir `ast.Attribute` |
| Atama | `ast.Assign`, hedefler `node.targets` |
| Sabit değer | `ast.Constant`, değeri `node.value` |
| Türsüz yakalama | `ast.ExceptHandler`, `node.type is None` |
| Satır numarası | `node.lineno` |

Bütün düğümleri gezmek: `ast.walk(ast.parse(kaynak))`. `ast.walk` satır
sırasıyla gezmez; sıra önemliyse sonuç `lineno` ile sıralanır.

## Akılda tutulacak

- `ast.parse` kodu çalıştırmaz; incelenen kod ne olursa olsun analiz
  güvenlidir.
- Metin araması yorum ve metinlerde yanlış alarm verir.
- Kabul edilen yanlış alarm kodda gerekçesiyle işaretlenir.
