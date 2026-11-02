Klasik şifrelerin tarihi, bugün de geçerli üç dersi tekrar tekrar gösterir.

## 1. "Kimse kıramaz" bir ölçüm değildir

Vigenère yüzyıllar boyunca çözülemez sanıldı. 19. yüzyılda Charles
Babbage ve Friedrich Kasiski, anahtarın tekrar etmesinin şifreli metinde
iz bıraktığını gösterdi; Kasiski yöntemini 1863'te yayımladı. Şifreyi
kullananlar bunu bilmediği için güvende olduklarını sanmaya devam etti.

Ders: bir algoritmaya güvenin kaynağı "henüz kıran olmadı" değil, **açıkça
yayımlanıp uzun süre saldırıya dayanmış olması**dır (Kriptografi Nedir?
bölümündeki Kerckhoffs ilkesi).

## 2. Kırılan çoğu zaman algoritma değil, kullanımdır

İkinci Dünya Savaşı'nda Alman ordusunun Enigma makinesi, elle yapılan
şifrelerden çok daha büyük bir anahtar uzayına sahipti. Çözülmesinde
makinenin yapısı kadar **kullanım hataları** da rol oynadı: tekrar eden
mesaj başlıkları, tahmin edilebilir kelimeler, aynı ayarın birden çok kez
kullanılması.

Ders: güçlü bir algoritma yanlış kullanılınca zayıflar. Bu modülün sonundaki
Sık Kriptografi Hataları bölümü bugünkü karşılıklarını anlatıyor: aynı
anahtarın tekrar kullanılması (XOR ve Tek Kullanımlık Şifre), tahmin
edilebilir rastgelelik (Rastgelelik), tekrarlanan başlangıç değeri.

## 3. Saldırgan senin düşündüğün yoldan gelmez

Yerine koyma şifresini kuran, 26! anahtarı kaba kuvvetle denemenin
imkânsız olduğunu düşünür ve haklıdır. Ama saldırgan kaba kuvvet
kullanmaz: harf sıklığına bakar. Güvenlik, savunanın hesapladığı en zor
yolla değil, saldırganın bulduğu **en kolay** yolla ölçülür.

## Bugün klasik şifreler nerede?

- Bulmacalarda, oyunlarda, eğitimde.
- ROT13 forumlarda cevabı gizlemek için.
- **Gerçek bir veriyi korumak için hiçbir yerde.** Bir programda Sezar,
  XOR ile sabit anahtar ya da "kendi şifremiz" görürsen, bu bir açıktır.
