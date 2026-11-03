Bellek hatalarıyla iki yoldan mücadele edilir: hatalı kodu bulup düzeltmek
ya da hatanın **yazılamayacağı** bir dil seçmek. İkincisi daha
kalıcıdır, çünkü bir programcının bir gün unutmasına bağlı değildir.

## Dil belleği nasıl korur?

- **Sınır denetimi:** her dizi erişiminde sıranın geçerli olup olmadığına
  bakılır (Python, Java, Go, Rust). Taşma, sessiz bozulma yerine bir
  hataya dönüşür.
- **Otomatik bellek yönetimi:** bellek, artık kimse kullanmayınca dil
  tarafından geri verilir (çöp toplayıcı: Python, Java, Go). Programcı
  geri vermeyi unutamaz ya da iki kez yapamaz.
- **Sahiplik kuralları:** Rust, her verinin tek bir sahibi olmasını ve
  ödünç alınan verinin sahibinden uzun yaşamamasını **derleme anında**
  denetler. Use-after-free ve double free içeren kod derlenmez.

## Bedeli ne?

| Yaklaşım | Kazanç | Bedel |
|---|---|---|
| C, C++ | En yüksek hız, donanıma yakınlık | Güvenlik programcıya kalır |
| Çöp toplayıcılı dil | Bellek hatası neredeyse yok | Biraz hız ve bellek |
| Rust | Hem hız hem güvenlik | Öğrenmesi daha zor, katı kurallar |

## Güvenli dilde de dikkat

- Python'un kendisi ve birçok paket C ile yazılmıştır; onlardaki taşma seni
  de etkiler. Paketleri güncel tutmak bu yüzden önemlidir (Bağımlılıklar ve
  Tedarik Zinciri bölümü).
- Rust'ta `unsafe` bloğu, derleyicinin denetimini o parça için kapatır.
  İncelemede `unsafe` bloklar ayrıca okunur.
- Bellek güvenliği **mantık hatalarını** engellemez: yanlış yetki denetimi,
  enjeksiyon ya da sızan parola güvenli dilde de olur.

## Eski kod ne olacak?

Milyonlarca satır C ve C++ kodu bir günde yeniden yazılamaz. Pratik yol
katmanlıdır:

1. Yeni kodu bellek güvenli bir dilde yaz.
2. Eski kodu koruma katmanlarıyla derle ve çalıştır (sonraki bölüm: ASLR,
   DEP, kanarya).
3. Tehlikeli fonksiyonları ara ve değiştir; statik analiz araçlarıyla
   tara.
4. En çok dışarıdan veri alan parçaları (ayrıştırıcılar, ağ kodu) önce
   yeniden yaz.
