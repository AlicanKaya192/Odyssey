İyi bir uyarı az çalar ama çaldığında bakmaya değer.

## Kurallar

- Her uyarının bir **sahibi** olsun: kim bakacak?
- Her uyarının yanında **ne yapılacağı** yazsın (kısa bir yönerge).
- Tek bir aşılmada değil, **üst üste birkaç aşılmada** çalsın
  (`patience`).
- Eşik, ölçünün normal dalgalanmasından geniş olsun: önce birkaç hafta
  izle, sonra eşiği koy.
- Aynı sorun için tek uyarı: bir sorun on uyarı doğurmasın.
- Kalite uyarısı (doğruluk) gecikmeli gelir; ona erken sinyallerden
  (girdi, tahmin oranı) en az biri eşlik etsin.

## Uyarı mı, bilgi mi?

| Durum | Uyarı (biri hemen bakmalı) | Panoda bilgi |
|---|---|---|
| Hata oranı birden %10 | Evet | |
| p95 gecikme biraz arttı | | Evet |
| Tahmin oranı iki aydır kayıyor | Evet | |
| Bir gün tahmin oranı biraz farklı | | Evet |
| Doğruluk eşiğin altında | Evet | |

## Yapma

- Her ölçüye uyarı koyma; uyarı sayısı arttıkça her birine gösterilen
  dikkat azalır.
- Uyarıyı otomatik yeniden eğitime bağlamadan önce, uyarıların ne kadar
  sık yanlış çaldığını ölç.
- Tahmin oranının artmasını tek başına "model bozuldu" diye okuma;
  müşteriler gerçekten değişmiş olabilir.
