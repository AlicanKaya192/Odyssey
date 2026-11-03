Bir kurum bildirimleri yalnızca beklemekle kalmaz; nasıl alacağını önceden
yazar. Bu yazılı kurallar **açıklama politikası** (vulnerability disclosure
policy) adıyla yayımlanır ve security.txt dosyasındaki `Policy` alanı ona
bağlanır.

## Politikada ne yazar?

| Bölüm | Örnek içerik |
|---|---|
| Kapsam | Hangi siteler ve uygulamalar; hangileri kapsam dışı |
| İzin verilenler | Kendi hesabınla, başkasının verisine dokunmadan doğrulamak |
| Yasaklar | Hizmeti yavaşlatmak ya da durdurmak, sosyal mühendislik, fiziksel erişim, veri indirmek |
| Nasıl bildirilir | Adres, şifreli iletişim yolu, rapor biçimi |
| Kurumun sözleri | Alındı bildirimi süresi, düzeltme takvimi paylaşımı, teşekkür |
| Güvenli liman | Kurallara uyan araştırmacıya hukuki yola gidilmeyeceği |
| Açıklama | Ne zaman ve nasıl birlikte duyurulacağı |

## Kurum tarafında süreç

1. **Al:** bildirimi tek bir kanaldan topla, alındığını kısa sürede söyle.
2. **Doğrula:** açığı kendi test ortamında yeniden üret.
3. **Önceliklendir:** etkiye ve önem derecesine göre sıraya koy.
4. **Düzelt:** düzeltmeyi yaz, sına, yayınla; benzer yerleri de ara
   (Kod İnceleme ve Statik Analiz bölümü).
5. **Duyur:** bulan kişiyle anlaşarak, düzeltmeyle birlikte; gerekirse
   CVE kimliği al.
6. **Öğren:** olay sonrası incelemeye ekle (Olay Müdahalesi bölümü).

## Bulan kişi için ölçülü davranış

- Kurum cevap vermezse önce başka bir resmî kanal dene; hemen herkese
  duyurma.
- Takvim konusunda esnek ol; karmaşık bir düzeltme zaman alabilir.
- Açık kapandıktan sonra elinde kalan notları ve ekran görüntülerini sil.
- Duyuruda kurumu küçük düşürmek değil, kullanıcıları korumak amaçtır.
