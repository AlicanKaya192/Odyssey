Parça parça çalışmanın temel sorusu: **parçaların sonuçlarından bütünün
sonucu çıkar mı?** Bazı hesaplar doğrudan birleşiyor, bazıları ancak başka
bir şey biriktirilirse, bazıları hiç.

## Doğrudan birleşenler

| Hesap | Parçada | Birleştirme |
|---|---|---|
| Toplam | `sum()` | topla |
| Sayı | `len()` / `count()` | topla |
| En küçük | `min()` | en küçüğünü al |
| En büyük | `max()` | en büyüğünü al |
| En büyük N | `nlargest(N)` | birleştir, yine `nlargest(N)` |

## Başka bir şey biriktirince birleşenler

| Hesap | Biriktir | Sonda |
|---|---|---|
| Ortalama | toplam, sayı | toplam / sayı |
| Varyans | sayı (n), toplam (s), kareler toplamı (q) | (q − s² / n) / (n − 1) |
| Farklı değer sayısı | görülen değerlerin kümesi | kümenin uzunluğu |
| Gruplu ortalama | gruplu toplam, gruplu sayı | böl |

Varyans formülü bu bölümde 300 000 satırda pandas'ın `var()` sonucuyla
dört ondalığına kadar aynı çıktı. (Çok büyük sayılarda bu formül yuvarlama
hatası biriktirebiliyor; daha sağlam yolları istatistik kütüphaneleri
kullanıyor.)

## Parçalardan kesin bulunamayanlar

| Hesap | Neden | Ne yapılır |
|---|---|---|
| Ortanca | Parça ortancalarının bütünün ortancasıyla ilişkisi yok | Bütün değerler gerekir ya da yaklaşık yöntem (Bölüm 9) |
| Yüzdelikler (ör. %95) | Aynı sebep | Yaklaşık yöntem |
| Ortalamaların ortalaması | Parça büyüklükleri farklıysa yanlış ağırlık | Toplam ve sayı biriktir |
| `nunique()` toplamı | Aynı değer birçok parçada sayılıyor | Küme kullan |

## Kontrol sorusu

Yeni bir hesap gördüğünde sor: "İki parçanın sonucunu bilsem, ikisinin
birleşiminin sonucunu bulabilir miyim?"

- Toplam: 10 + 20 = 30. Evet.
- Ortalama: 5 ve 7 bilmek yetmez; kaç satırdan geldiklerini de bilmek
  gerek. Toplam ve sayı biriktirince evet.
- Ortanca: 5 ve 7 bilmek, birleşimin ortancası hakkında çok az şey söylüyor.
  Hayır.
