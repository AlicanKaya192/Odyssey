## Program ve sistem

| Konu | Akılda tutulacak |
|---|---|
| Bellek | Yazmadan önce ölç; korumalar (ASLR, DEP, kanarya) hatayı düzeltmez |
| İşletim sistemi | Standart hesap, süreç yalıtımı, varsayılan ret, sıkılaştırma |
| Dosya izinleri | `644` dosya, `755` program, `600` gizli; herkese yazılabilir dosya bulgudur |
| Yetki yükseltme | Her istekte sahiplik; istemciden gelen alana izin listesi |

## Yazılım

| Konu | Akılda tutulacak |
|---|---|
| Güvenli geliştirme | Sola kaydır; güvenli başarısız ol; güvenli varsayılan |
| Kod inceleme | `ast.parse` kodu çalıştırmadan okur; araç kalıbı, insan anlamı denetler |
| Bağımlılıklar | Sabit sürüm, duyurularla karşılaştırma, kilit dosyasında özet |
| Sırlar | Koda ve depoya yazılmaz; sızınca önce döndürülür |

## Operasyon

| Konu | Akılda tutulacak |
|---|---|
| Kayıt | Yapılı, UTC, sır ve kişisel veri yok |
| Tespit | İmza bileni, anomali yeniyi bulur; kesinlik ve duyarlılık |
| Olay müdahalesi | Hazırlık, tespit, sınırlama, temizleme, kurtarma, ders |
| Adli bilişim | Önce özet al; gözetim zinciri; uçuculuk sırası |
| Yedek | 3-2-1; RPO veri kaybı, RTO kesinti; geri yüklemeyi dene |
| Bulut | Paylaşılan sorumluluk; IAM'de varsayılan ret, ret kazanır |

## İnsan ve kural

| Konu | Akılda tutulacak |
|---|---|
| Gizlilik | Amaç, en az veri, takma ad (HMAC), k-anonimlik, saklama süresi |
| Etik ve hukuk | Yazılı izin, kapsam, zaman penceresi; hukuki tavsiye değil |
| Sorumlu açıklama | Dur, gizlice bildir, düzeltmeyle birlikte duyur |

## Python kalıpları

- Sabit zamanlı karşılaştırma: `hmac.compare_digest(a, b)`.
- Dosya özeti: `hashlib.sha256(data).hexdigest()`.
- Anahtarlı özet: `hmac.new(key, value, hashlib.sha256).hexdigest()`.
- Güvenli rastgele: `secrets.token_urlsafe(32)`.
- UTC'ye çevirmek: `datetime.fromisoformat(s).astimezone(timezone.utc)`.
- Sayım: `Counter(...)`, eşik: `[k for k, n in c.items() if n >= limit]`.
- Ağ içinde mi: `ipaddress.ip_address(a) in ipaddress.ip_network(cidr)`.
- Kodu çalıştırmadan okumak: `ast.walk(ast.parse(source))`.
