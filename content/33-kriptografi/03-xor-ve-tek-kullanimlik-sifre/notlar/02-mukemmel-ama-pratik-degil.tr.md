Tek kullanımlık şifre mükemmel gizlilik sağlayan tek yöntemdir; buna
rağmen gündelik kullanımda neredeyse hiç görülmez. Nedenleri, modern
kriptografinin neden "yeterince güvenli"yi seçtiğini anlatır.

## Anahtar dağıtım sorunu

Anahtar mesaj kadar uzun olduğu için, göndereceğin her bayt için önceden
bir bayt anahtarı karşı tarafa **güvenli bir yoldan** ulaştırman gerekir.
Diplomatik çantalarla taşınan kâğıt sayfalar bu yüzden kullanıldı. Bir
web sitesi her ziyaretçisine önceden bu kadar anahtar gönderemez.

## Saklama ve imha

Kullanılmış anahtar sayfası hemen yok edilmeli, kullanılmamışlar gizli
tutulmalıdır. İki tarafın anahtar sırasını kaçırmaması gerekir; bir sayfa
atlanırsa sonraki bütün mesajlar okunamaz.

## Gerçek rastgelelik

Anahtar bir programın `random` modülüyle üretilirse koşul 1 çiğnenir ve
kanıt geçersiz olur. Rastgelelik bölümünde `random`'ın neden tahmin
edilebilir olduğunu göreceğiz.

## Modern çözüm: hesaplamaya dayalı güvenlik

Modern şifreler mükemmel gizlilik iddia etmez. Bunun yerine **hesaplamaya
dayalı güvenlik** (computational security) sağlar: kısa (128 ya da 256
bitlik) bir anahtarla, bilinen her saldırının evrenin ömründen uzun
sürmesi. Kriptografi Nedir? bölümündeki kaba kuvvet hesabı bunun ölçüsüdür.
Bu sayede tek bir kısa anahtarla gigabaytlarca veri şifrelenebilir ve
anahtar asimetrik yöntemlerle (Diffie-Hellman ve Eliptik Eğriler bölümü)
güvensiz bir ağ üzerinden bile kararlaştırılabilir.

| | Tek kullanımlık şifre | Modern simetrik şifre |
|---|---|---|
| Güvenlik | Mükemmel (kanıtlı) | Hesaplamaya dayalı |
| Anahtar uzunluğu | Mesaj kadar | 128–256 bit |
| Anahtar tekrar kullanılabilir mi? | Asla | Evet (her mesajda yeni nonce ile) |
| Bütünlük | Yok | Doğrulanmış kiplerde var |
| Pratik mi? | Çok özel durumlar | Her yerde |
