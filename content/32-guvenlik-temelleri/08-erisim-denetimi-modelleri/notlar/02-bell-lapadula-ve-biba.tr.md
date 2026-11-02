İki model aynı sıralı düzeyleri kullanır ama farklı şeyi korur ve kuralları
birbirinin tersidir.

| | **Bell-LaPadula** | **Biba** |
|---|---|---|
| Neyi korur? | Gizlilik | Bütünlük |
| Okuma kuralı | Yukarı okuma yok: düzey ≥ belge | Aşağı okuma yok: düzey ≤ belge |
| Yazma kuralı | Aşağı yazma yok: düzey ≤ belge | Yukarı yazma yok: düzey ≥ belge |
| Korkulan şey | Gizli bilginin aşağı akması | Güvenilmez verinin yukarı akması |

## Ezberlemek yerine akışı düşün

- **Bell-LaPadula:** bilgi yalnızca **yukarı** akabilir. Gizli bilgi
  aşağıdaki birinin eline geçmesin.
- **Biba:** bilgi yalnızca **aşağı** akabilir. Az güvenilir bir kaynaktan
  gelen veri, çok güvenilir bir sistemi bozmasın.

## Bell-LaPadula örneği

Düzeyler: `public` < `internal` < `secret` < `top-secret`. Yetki düzeyi
`secret` olan biri için:

| Belge | Okuyabilir mi? | Yazabilir mi? |
|---|---|---|
| public | Evet | Hayır |
| internal | Evet | Hayır |
| secret | Evet | Evet |
| top-secret | Hayır | Evet |

"Yukarı yazmak" pratikte bir rapor kutusuna belge bırakmaya benzer: üst
düzeydeki birinin okuyacağı yere yazarsın, ama orayı okuyamazsın.

## Biba örneği

Düzeyler: `low` (internetten gelen dosya) < `medium` (çalışanın belgesi) <
`high` (sistem yapılandırması). `medium` düzeyindeki bir program için:

| Veri | Okuyabilir mi? | Yazabilir mi? |
|---|---|---|
| low | Hayır | Evet |
| medium | Evet | Evet |
| high | Evet | Hayır |

## Neden ikisi birden zor?

İki model aynı düzeylerle birlikte uygulanırsa kişi yalnızca **kendi
düzeyinde** okuyup yazabilir. Bu çok katıdır; bu yüzden gerçek sistemler
gizlilik ve bütünlük için ayrı etiketler kullanır.
