| Katman | Ölçü | Ne zaman | Örnek eşik |
|---|---|---|---|
| Sistem | p95 gecikme | Hemen | 200 ms'nin üstü |
| Sistem | Hata oranı (`5xx`) | Hemen | %1'in üstü |
| Girdi | Sütun ortalaması | Hemen | Eğitimdekinden belirgin uzak |
| Girdi | Şemaya uymayan istek (`422`) | Hemen | %2'nin üstü |
| Tahmin | "Gidecek" oranı | Hemen | Başlangıçtan 0,1 uzak, iki ay üst üste |
| Kalite | Doğruluk | Etiket gelince | 0,75'in altı |

## Dersteki sekiz ay

| Ay | Tahmin oranı | Kullanım | Doğruluk |
|---|---|---|---|
| 0 | 0,204 | 32,0 | 0,813 |
| 3 | 0,390 | 27,5 | 0,784 |
| 4 | 0,498 | 25,0 | 0,673 |
| 7 | 0,590 | 21,5 | 0,658 |

Tahmin oranı uyarısı 3. ayda çaldı; doğruluk 4. ayda düştü ve bu ancak
5. ayda bilinebildi.

## Tahmin kaydında ne olur?

| Alan | Neden |
|---|---|
| Müşteri kimliği | Gerçek sonuçla birleştirmek için |
| Zaman (ay, gün) | Zamana göre gruplamak için |
| Model sürümü | Sürüm sürüm kalite |
| Tahmin (olasılık) | Dağılımı izlemek ve doğruluğu hesaplamak için |
| Girdiler (ya da bir örneği) | Eğitim-sunma farkını yakalamak için |

## Terimler

- **İzleme** (monitoring): canlıdaki modelin sağlığını sürekli ölçmek.
- **Tahmin kaydı** (prediction log): her tahminin kimlik, sürüm ve
  zamanla birlikte yazıldığı kayıt.
- **Gecikmeli etiket** (delayed label): gerçek sonucun tahminden sonra,
  geç gelmesi.
- **Uyarı yorgunluğu** (alert fatigue): çok sık çalan uyarıların
  görmezden gelinmesi.
