Hayali bir okul API'sinin belgesini REST gözüyle okuyalım.

## Belge

```text
GET    /students                 bütün öğrenciler
GET    /students/17              bir öğrenci
POST   /students                 yeni öğrenci
PATCH  /students/17              öğrencinin bir alanını değiştir
DELETE /students/17              öğrenciyi sil
GET    /students/17/grades       öğrencinin notları
POST   /students/17/grades       öğrenciye not ekle
GET    /courses?teacher=ada      Ada'nın dersleri
POST   /sendReportCard           karne gönder
GET    /students/17/remove       öğrenciyi kaldır
```

## Değerlendirme

İlk sekiz satır REST'e uygun: çoğul koleksiyonlar, kimlikle öğeler, iç içe
ilişki (`/students/17/grades`), süzme sorguda (`?teacher=ada`).

Son iki satırda sorun var:

- `POST /sendReportCard`: adreste fiil. REST'te bir eylemi kaynağa
  çevirmek gerekir: "karne gönderimi" bir kaynak olabilir:
  `POST /students/17/report-cards`.
- `GET /students/17/remove`: `GET` bir şeyi siliyor. Bir tarayıcı bu
  adresi önceden yüklese ya da bir arama motoru gezse öğrenci silinir.
  Doğrusu zaten belgede var: `DELETE /students/17`.

## Eylemi kaynağa çevirmek

Bazı işler "isim" gibi durmuyor: e-posta göndermek, ödeme yapmak, raporu
yeniden üretmek. REST'te bunlar genellikle **oluşturulan bir kayıt** olarak
düşünülür:

| Eylem | Kaynak olarak |
|---|---|
| Karne gönder | `POST /report-cards` |
| Ödeme yap | `POST /payments` |
| Şifreyi sıfırla | `POST /password-resets` |
| Raporu yeniden üret | `POST /reports/7/runs` |

Böylece her işin bir kaydı olur ve `GET /payments/123` ile durumuna
bakılabilir.
