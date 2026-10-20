Özellik deposunun parçaları:

<figure class="fig">
  <div class="versus">
    <div><h4>Çevrim dışı depo</h4>Her özelliğin tarihli geçmişi. Eğitim verisi etiket tarihi itibarıyla çekilir. Büyük, yavaş olabilir.</div>
    <div><h4>Çevrim içi depo</h4>Her müşterinin son değerleri. Sunma anında kimlikle okunur. Küçük, milisaniyeler içinde.</div>
  </div>
  <figcaption>İkisi aynı tanımlardan ve aynı yazılardan beslenir.</figcaption>
</figure>

## Bir özelliğin tanımı

| Alan | Örnek |
|---|---|
| Ad | `support_calls_30d` |
| Varlık (kime ait) | Müşteri kimliği |
| Hesap | Son 30 gündeki destek araması sayısı |
| Tür | Tam sayı |
| Tazelik | Günde bir |
| Sahibi | Müşteri verisi ekibi |

## "As of" birleştirmesi

Eğitim tablosunun her satırında bir müşteri ve bir **etiket tarihi**
var. Her özellik için o tarihten **önceki ya da o günkü** son değer
alınır; sonraki değerler yok sayılır.

| Müşteri | Etiket tarihi | Arama geçmişi | Kullanılan değer |
|---|---|---|---|
| C7 | 2026-02-15 | 01-01: 0, 02-01: 1, 03-01: 4 | 1 |
| C7 | 2026-03-10 | aynı | 4 |
| C7 | 2025-12-31 | aynı | yok (`None`) |

## Kontrol listesi

- Eğitim ve sunma özellikleri aynı tanımdan mı geliyor?
- Her eğitim satırının bir etiket tarihi var mı? Özellikler o tarih
  itibarıyla mı çekiliyor?
- Sunma anındaki özellik vektörü kaydediliyor mu?
- Tarihler `YYYY-AA-GG` biçiminde ve aynı saat diliminde mi?

## Yapma

- Özellik kodunu sunma için yeniden yazma.
- Eğitim verisini "bugünkü" tablodan çekip geçmiş etiketlere bağlama;
  geleceği görmüş olursun.
- Testi eğitimle aynı yanlış özellikle kurup sonucuna güvenme.
