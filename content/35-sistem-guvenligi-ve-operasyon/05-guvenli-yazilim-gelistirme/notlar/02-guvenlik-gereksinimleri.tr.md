Güvenli SDLC'nin ilk adımı, en çok atlanan adımdır: güvenliği bir
**gereksinim** olarak yazmak. "Uygulama güvenli olmalı" bir gereksinim
değildir; sınanamaz. İyi bir güvenlik gereksinimi, bir testin geçip
geçmediğine bakarak doğrulanabilen bir cümledir.

## Kötü ve iyi gereksinim

| Kötü | İyi |
|---|---|
| Uygulama güvenli olmalı | Yalnızca gönderinin yazarı ya da yönetici gönderiyi silebilir |
| Parolalar korunmalı | Parolalar yavaş, tuzlu bir özetle saklanır; düz metin hiçbir yere yazılmaz |
| Oturumlar güvenli olmalı | Oturum 30 dakika işlem yapılmayınca sona erer |
| Girdiler denetlenmeli | Miktar alanı yalnızca 1 ile 100 arasındaki tam sayıları kabul eder |

İyi gereksinimin ortak özelliği: kim, ne, hangi koşulda ve **ne olmamalı**
açıkça yazılı.

## Gereksinimden teste

Her güvenlik gereksiniminin en az bir testi olur. Gereksinimler bir
listeye kimlik numarasıyla yazılır, testler de hangi gereksinimi
sınadıklarını belirtir. Böylece **testi olmayan gereksinim** bir bakışta
görülür. Bu eşleştirmeye **izlenebilirlik** (traceability) denir.

| Gereksinim | Test |
|---|---|
| SEC-1: yalnızca yazar ya da yönetici siler | `stranger cannot delete`, `admin can delete` |
| SEC-2: oturum 30 dakikada biter | `session expires after 30 minutes` |
| SEC-3: miktar 1–100 | `quantity rejects 0`, `quantity rejects 250` |

## Gereksinimlerin kaynakları

- **Tehdit modeli:** her önemli tehdit için bir önlem, her önlem için bir
  gereksinim.
- **Yasa ve sözleşme:** kişisel veri (Gizlilik ve Veri Koruma bölümü),
  sektör kuralları.
- **Standartlar:** kurumun güvenlik politikası (Güvenlik Politikası ve
  Standartlar bölümü), yaygın kontrol listeleri.
- **Geçmiş olaylar:** bir kez yaşanan hata bir gereksinime ve bir teste
  dönüşür, böylece tekrar edemez.

## Önceliklendirme

Bulunan her güvenlik sorunu aynı aciliyette değildir. Ekipler bulguları
önem derecesine göre (kritik, yüksek, orta, düşük) sıralar ve
düzeltmeleri bu sırayla yapar. Önemli olan sıranın **yazılı bir kurala**
dayanmasıdır: "kritik bulgu yayını durdurur, düşük bulgu bir sonraki
sürüme kalabilir" gibi.
