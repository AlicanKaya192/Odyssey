Bir MLOps hattını canlıya almadan önce bu listeden geç.

## Veri

- Eğitim verisi tarih itibarıyla mı çekiliyor (Eğitim-Sunma Farkı)?
- Şema ve aralık kuralları yazılı mı, hatalı satır payı için eşik var mı?
- Ret olunca bir uyarı gidiyor mu?

## Eğitim ve kapı

- Eğitim sabit tohumla ve sabit kütüphane sürümleriyle mi?
- Kapının kümesi güncel, etiketli ve eğitim verisinden ayrı mı?
- Aday canlı modelden en az bir `MIN_GAIN` kadar iyi olmalı mı?
- Kapının kümesi eğitim verisiyle aynı kaynaktan geliyorsa, o kaynak da
  doğrulanıyor mu?

## Kayıt ve yayın

- Her sürüm verisinin özetiyle, ölçümleriyle ve eşiğiyle kayıtta mı?
- Yeni sürüm gölge ve kanaryadan geçiyor mu?
- Geri dönüş tek bir komut mu (önceki sürüme etiket)?

## İzleme

- Kayma (PSI) her gün, doğruluk etiketler gelince ölçülüyor mu?
- Kalibrasyon farkı ve iş ölçüsü izleniyor mu?
- Tetik eşikleri (`MAX_DROP`, `MAX_DRIFT`) adlarıyla yazılı mı?

## Dersteki eşikler

| Ad | Değer | Anlamı |
|---|---|---|
| `MAX_DROP` | 0,05 | Kapı skorundan bu kadar düşüş yeniden eğitimi tetikler |
| `MAX_DRIFT` | 0,25 | Bir sütunun PSI'si bunu aşarsa tetik |
| `MAX_INVALID` | 0,05 | Penceredeki geçersiz satır payı bunu aşarsa ret |
| `MIN_GAIN` | 0,003 | Aday en az bu kadar iyi değilse dışarıda kalır |
