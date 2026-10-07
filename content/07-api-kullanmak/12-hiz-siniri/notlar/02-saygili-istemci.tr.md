Bir API'yi hem kendin hem başkaları için sorunsuz kullanmanın alışkanlıkları.

## İstek sayısını azalt

- **Süzmeyi sunucuya bırak:** `?author=Austen` bütün listeyi indirip süzmekten
  çok daha az istek.
- **Büyük sayfa iste:** sınırı aşmadan `per_page`'i büyüt.
- **Sonuçları sakla:** aynı veriyi aynı gün beş kez isteme; bir kez al,
  dosyaya yaz (Bölüm 15).
- **Yalnızca değişeni iste:** API destekliyorsa `?since=2024-03-01` gibi
  parametrelerle yalnızca yeni kayıtları çek.

## Hızını ayarla

- İstekler arasında sınırın gerektirdiği kadar bekle.
- Gece çalışan büyük işlerde daha da yavaş git; acelen yok.
- Paralel istek (aynı anda birçok istek) atacaksan toplam hızı hesapla.

## Kendini tanıt

- `User-Agent` başlığına programının adını ve bir iletişim bilgisi yaz.
- Sorun çıkarsa API'nin sahibi seni engellemek yerine sana ulaşabilir.

## Kurallara uy

- `Retry-After`'a uy; daha erken dönme.
- API'nin kullanım koşullarını oku: bazı API'ler verinin nasıl
  kullanılabileceğini, saklanabileceğini de sınırlar.
- Sınırı aşmanın yollarını (birden çok anahtar, kimlik gizleme) arama; bu
  koşulların ihlalidir ve anahtarın iptaline yol açar.
