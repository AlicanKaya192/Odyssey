## Parçalar

| Parça | Görevi |
|---|---|
| Çözümleyici (resolver) | Bilgisayarın sorduğu sunucu; zinciri izler, önbellekte tutar |
| Kök ve TLD sunucuları | "Bu alanın yetkili sunucusu şurada" der |
| Yetkili sunucu | Alanın kayıtlarının asıl sahibi |
| TTL | Cevabın önbellekte kalacağı süre (saniye) |
| `NXDOMAIN` | "Böyle bir ad yok" cevabı |

## Kayıt türleri

| Tür | Anlamı |
|---|---|
| A / AAAA | IPv4 / IPv6 adresi |
| CNAME | Takma ad; hedef adla devam |
| MX | E-posta sunucusu |
| NS | Yetkili sunucular |
| TXT | Serbest metin (doğrulama kuralları vb.) |
| DS | Alt alanın anahtar özeti (DNSSEC) |

## Saldırı ve savunma

| Risk | Savunma |
|---|---|
| Önbellek zehirleme | Rastgele sorgu numarası ve kaynak port; DNSSEC |
| Sorguların dinlenmesi | Şifreli DNS (DoT, DoH) |
| DNS ayarının ele geçirilmesi | Yönlendirici parolası ve güncelleme |
| Alan adı hesabının ele geçirilmesi | MFA, hesap kilidi |
| Sahipsiz CNAME (alt alan devralma) | Kapatılan hizmetin kaydını da silmek |
| Benzer adlar | İzleme, yer imi kullanmak |

## Kurallar

- DNSSEC **bütünlük** sağlar, **gizlilik** sağlamaz; şifreli DNS tersini.
- Önbelleğe giren yanlış cevap **TTL bitene kadar** herkese verilir.
- DNS kayıtları da bir varlıktır: sahibi ve gözden geçirme takvimi olur.
