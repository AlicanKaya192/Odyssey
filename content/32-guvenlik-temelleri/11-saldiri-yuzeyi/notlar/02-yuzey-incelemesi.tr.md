Bir web uygulamasının saldırı yüzeyini incelemek için adım adım bir yol.
Bunu kendi yazdığın ya da sorumlu olduğun bir sistemde yaparsın; başkasının
sistemini izinsiz taramak etik ve hukuk dışıdır (Etik ve Hukuk bölümü).

## 1. Listeyi çıkar

Kaynaklardan derle, tek birine güvenme:

- Uygulamanın kendi yönlendirme (route) tanımları.
- Sunucu ve ağ ayarlarında açık olan hizmetler.
- Son üç ayın erişim kayıtlarında görülen adresler.
- Ekibin bildiği ama kodda bulunmayanlar (eski sunucular, test ortamları).

Kayıtlarda görünen ama kodda olmayan bir adres, birinin unuttuğu ya da
habersiz açtığı bir kapıdır.

## 2. Her satırı doldur

| Giriş noktası | Kim ulaşır? | Giriş şart mı? | Ne alır? | Kullanılıyor mu? | Sahibi |
|---|---|---|---|---|---|
| `/login` | İnternet | Hayır (giriş sayfası) | Kullanıcı adı, parola | Çok | Ayşe |
| `/search` | İnternet | Hayır | Arama metni | Orta | Can |
| `/admin` | İnternet | Evet | Her şey | Az | Ayşe |
| `/legacy-upload` | İnternet | Evet | Dosya | Hiç | Bilinmiyor |

## 3. Karar ver

- **Kullanılmıyor ve sahibi yok:** kaldır (`/legacy-upload`).
- **Az kullanılıyor ama güçlü:** ulaşılabilirliği daralt (`/admin` →
  yalnızca iç ağ).
- **Giriş istemeyen ve dış veri alan:** girdi doğrulama ve hız sınırı
  öncelikli (`/search`, `/login`).

## 4. Tekrarla

İnceleme bir kez yapılıp bitmez. Her sürümde yeni uç noktaların listesi
çıkarılır, her çeyrekte kayıtlarla karşılaştırılır. Fark listesi küçük
olduğunda inceleme de kısa sürer.
