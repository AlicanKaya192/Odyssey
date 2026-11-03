## 2021 listesi ve temel savunma

| No | Kategori | Temel savunma | Ayrıntı |
|---|---|---|---|
| A01 | Bozuk erişim denetimi | Her istekte sahiplik ve yetki denetimi; varsayılan reddet | Yetkilendirme bölümü |
| A02 | Kriptografik hatalar | TLS, yavaş tuzlu parola özeti, `secrets` | Kriptografi modülü |
| A03 | Enjeksiyon | Parametreli sorgu, bağlama uygun çıktı kodlama | SQL Enjeksiyonu, XSS |
| A04 | Güvensiz tasarım | Tehdit modelleme, hız sınırı, kötüye kullanım senaryoları | Tehdit Modelleme |
| A05 | Yapılandırma hataları | Güvenli varsayılan, yayın öncesi otomatik denetim | Bu bölüm |
| A06 | Açıklı ve eski bileşenler | Bileşen listesi, düzenli güncelleme | Bağımlılıklar |
| A07 | Kimlik doğrulama hataları | MFA, hız sınırı, iyi oturum yönetimi | Kimlik Doğrulama Hataları |
| A08 | Bütünlük hataları | Özet ve imza doğrulaması | Dijital İmza |
| A09 | Kayıt ve izleme hataları | Olayları kaydet, sırları maskele, uyarı kur | Kayıt ve İzleme |
| A10 | SSRF | Hedef için izin listesi, adresi ayrıştırarak denetim | SSRF |

## Bu bölümün kalıpları

- **Sahiplik:** `if invoice is None or invoice["owner"] != user: return None`.
- **Parametreli sorgu:** `conn.execute("... WHERE name = ?", (name,))`.
- **Sürüm karşılaştırma:** `tuple(int(p) for p in version.split("."))`;
  metin olarak karşılaştırma.
- **Bütünlük:** `hashlib.sha256(data).hexdigest() == expected` (özet
  güvenilir kanaldan).
- **Maskeleme:** `re.sub(r"(password|token)=[^&\s]+", r"\1=***", line)`.

## Akılda tutulacak cümleler

- Kimlik doğrulama "kimsin?", erişim denetimi "buna yetkin var mı?"
  sorusudur; ikisi ayrı ayrı sorulur.
- Veri kod gibi yorumlanmaz.
- Varsayılan ayar güvenli ayardır.
- Dışarıdan gelen hiçbir şey doğrulanmadan kullanılmaz.
- Kayıt olayı yazar, sırrı yazmaz.
