## 2025 listesi ve temel savunma

| No | Kategori | Temel savunma | Ayrıntı |
|---|---|---|---|
| A01 | Bozuk erişim denetimi (CSRF, SSRF dahil) | Her istekte sahiplik ve yetki denetimi; varsayılan reddet | Yetkilendirme, CSRF, SSRF |
| A02 | Yapılandırma hataları | Güvenli varsayılan, yayın öncesi otomatik denetim | Bu bölüm |
| A03 | Tedarik zinciri hataları | Bileşen listesi, düzenli güncelleme, sabit sürüm, güvenilir kaynak | Bağımlılıklar |
| A04 | Kriptografik hatalar | TLS, yavaş tuzlu parola özeti, `secrets` | Kriptografi modülü |
| A05 | Enjeksiyon | Parametreli sorgu, bağlama uygun çıktı kodlama | SQL Enjeksiyonu, XSS |
| A06 | Güvensiz tasarım | Tehdit modelleme, hız sınırı, kötüye kullanım senaryoları | Tehdit Modelleme |
| A07 | Kimlik doğrulama hataları | MFA, hız sınırı, iyi oturum yönetimi | Kimlik Doğrulama Hataları |
| A08 | Bütünlük hataları | Özet ve imza doğrulaması | Dijital İmza |
| A09 | Kayıt ve uyarı hataları | Olayları kaydet, sırları maskele, uyarı kur | Kayıt ve İzleme |
| A10 | Olağandışı durumlar | Kapalı kalarak başarısız ol; beklenen hatayı açıkça yakala | Bu bölüm |

2021 sürümünden farklar: tedarik zinciri (eski "açıklı ve eski
bileşenler") ve olağandışı durumlar yeni; SSRF ayrı kategori olmaktan
çıkıp A01'e girdi; enjeksiyon A03'ten A05'e, yapılandırma A05'ten A02'ye
geçti.

## Bu bölümün kalıpları

- **Sahiplik:** `if invoice is None or invoice["owner"] != user: return None`.
- **Parametreli sorgu:** `conn.execute("... WHERE name = ?", (name,))`.
- **Sürüm karşılaştırma:** `tuple(int(p) for p in version.split("."))`;
  metin olarak karşılaştırma.
- **Bütünlük:** `hashlib.sha256(data).hexdigest() == expected` (özet
  güvenilir kanaldan).
- **Maskeleme:** `re.sub(r"(password|token)=[^&\s]+", r"\1=***", line)`.
- **Kapalı kalmak:** `except KeyError: return False`; geniş
  `except Exception: return True` yok.

## Akılda tutulacak cümleler

- Kimlik doğrulama "kimsin?", erişim denetimi "buna yetkin var mı?"
  sorusudur; ikisi ayrı ayrı sorulur.
- Veri kod gibi yorumlanmaz.
- Varsayılan ayar güvenli ayardır.
- Dışarıdan gelen hiçbir şey doğrulanmadan kullanılmaz.
- Kayıt olayı yazar, sırrı yazmaz.
- Hata çıkınca cevap "hayır"dır.
