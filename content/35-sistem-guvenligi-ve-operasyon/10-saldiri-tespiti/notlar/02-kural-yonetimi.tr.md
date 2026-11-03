Bir tespit sistemi, kurallarıyla iyidir. Kural yazmak kolaydır; zor olan,
yüzlerce kuralı yararlı ve sessiz tutmaktır. Bu not tespit kurallarının
yaşam döngüsünü topluyor.

## Bir kuralın yaşam döngüsü

1. **İhtiyaç:** hangi tehdidi yakalamak istiyoruz? Tehdit modeli ya da
   yaşanmış bir olay bir kurala dönüşür.
2. **Yazmak:** kalıp, eşik ya da örüntü; neyi yakalayacağı ve neyi
   yakalamayacağı yazılır.
3. **Sınamak:** kural önce geçmiş kayıtlar üzerinde çalıştırılır: kaç uyarı
   üretirdi, bunların kaçı gerçekti?
4. **Uyarı kipinde yayın:** kural bir süre yalnızca uyarır; engellemez.
5. **Ayarlamak:** yanlış alarmlara bakılır, eşik ve kalıp düzeltilir.
6. **Gözden geçirmek:** kimsenin yanıtlamadığı ya da yıllardır hiç
   tetiklenmeyen kural sorgulanır.

## Her uyarının bir yanıtı olmalı

Bir uyarı geldiğinde ne yapılacağı yazılı değilse, uyarı ya görmezden
gelinir ya da herkes başka bir şey yapar. Her kuralın yanında kısa bir
**yanıt kılavuzu** (playbook) durur:

| Alan | Örnek |
|---|---|
| Uyarı | Başarısız girişlerin ardından başarılı giriş |
| Önem | Yüksek |
| İlk bakılacaklar | Aynı adresten başka hesaplara deneme var mı? Giriş sonrası ne yapıldı? |
| İlk adım | Hesabın oturumlarını kapat, parolayı sıfırlat |
| Kime bildirilir | Güvenlik ekibi, hesap sahibi |

## Uyarıları gruplamak

Aynı kaynaktan kısa sürede gelen yüz uyarı, yüz ayrı iş değil tek bir
olaydır. Uyarılar kaynağa (adres, hesap, makine) ve zamana göre
gruplanır: iki uyarı arasındaki boşluk belirli bir süreden kısaysa aynı
olaya eklenir. Böylece ekip uyarı sayısına değil olay sayısına bakar.

## Tespitin sınırları

- Tespit sistemi yalnızca **gördüğüne** bakar: şifreli trafiğin içini ya da
  kaydı tutulmayan bir sistemi göremez.
- Her kural bir varsayıma dayanır; varsayım değişince (yeni bir uygulama,
  yeni bir iş saati) kural da gözden geçirilir.
- Tespit, önlemin yerini tutmaz: önce kapıları kapatmak, sonra kapıları
  izlemek gerekir.
