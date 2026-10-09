API Kullanmak modülü bitti. Öğrendiklerini kalıcı yapmanın ve bir sonraki adıma geçmenin
yolları.

## Gerçek API'lerle pratik

Alıştırma sunucusunda öğrendiğin her şey gerçek API'lerde de geçerli. Başlamak
için iyi adaylar:

- **Anahtarsız açık API'ler:** hava durumu, ülke bilgileri, açık veri
  portalları gibi kayıt istemeyen servisler. İlk denemeler için ideal.
- **GitHub API'si:** belgesi çok iyi; anahtarsız düşük bir hız sınırıyla
  çalışıyor, anahtarla sınır yükseliyor. Sayfalama, hız sınırı başlıkları ve
  kimlik doğrulamanın hepsini gerçek hâliyle görürsün.
- **Kendi alanındaki veri:** ilgilendiğin konunun (spor, finans, ulaşım)
  açık API'sini bul; o veriyle küçük bir veri seti kur.

Her yeni API'de aynı sırayı izle: belgeyi oku, tarayıcıda ya da curl/Postman ile
dene, sonra Python'a dök.

## Küçük bir proje fikri

1. Açık bir API seç.
2. Bölüm 15'teki hat şablonunu ona uyarla: çek, sakla, düzleştir, denetle,
   yaz.
3. Veri setini pandas ile aç ve bir soru sor ("en çok hangisi?", "zamanla
   nasıl değişti?").
4. Hattı bir hafta boyunca her gün artımlı çalıştır; değişimi gör.

## Sıradaki patikalar

- **FastAPI ile REST API yazmak:** masanın öbür tarafı. Kendi
  uç noktalarını yazacak, Pydantic ile doğrulama yapacak, `/docs`'ta Swagger
  UI'ını göreceksin; patikanın sonunda bir makine öğrenmesi modelini API
  arkasına koyacaksın.
- **Docker:** yazdığın API'yi her bilgisayarda aynı çalışan bir pakete
  koymak.

## Akılda kalsın

> Önce kod, sonra gövde. Her isteğe süre. Yalnızca geçici hatayı yeniden dene.
> Anahtar koda girmez. Ham veriyi sakla.
