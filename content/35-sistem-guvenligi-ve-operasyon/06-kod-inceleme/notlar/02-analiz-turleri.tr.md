Statik analiz, kodu güvenlik açısından sınamanın yollarından yalnızca
biridir. Her yöntem başka bir şeyi görür ve başka bir şeyi kaçırır; bu
yüzden birlikte kullanılırlar.

## Yöntemler

| Yöntem | Ne yapar? | Güçlü yanı | Zayıf yanı |
|---|---|---|---|
| Statik analiz (SAST) | Kodu çalıştırmadan okur | Erken, her satıra bakar | Yanlış alarm, niyeti bilmez |
| Dinamik analiz (DAST) | Çalışan uygulamaya dışarıdan istek gönderir | Gerçek davranışı görür | Kodun yalnızca ulaşılan kısmı |
| Bağımlılık taraması (SCA) | Kullanılan paketleri bilinen açıklarla karşılaştırır | Başkasının açığını bulur | Yalnızca bilinen açıklar |
| Sır taraması | Kodda ve geçmişte parola, anahtar arar | Sızıntıyı erken yakalar | Biçimi bilinmeyen sırrı kaçırır |
| Kod inceleme | İnsan okur | Mantık hatasını görür | Yorulur, yavaştır |

## Yanlış alarm ve kaçırılan bulgu

Her denetim iki türlü yanılır: olmayan bir sorunu bildirir (**yanlış
alarm**, false positive) ya da olan bir sorunu kaçırır (**kaçırılan
bulgu**, false negative). Kuralları sıkılaştırmak birincisini, gevşetmek
ikincisini artırır. İyi bir araç ayarı, ekibin gerçekten okuyabileceği
sayıda bulgu üretir.

## Bulguyu kabul etmek

Bir bulgu incelenip yanlış alarm olduğuna karar verilirse, araç bir
sonraki taramada aynı şeyi yeniden bildirmesin diye işaretlenir. Bu işaret
kodun içinde, gerekçesiyle ve kimin karar verdiğiyle durur. Gerekçesiz
toplu susturma, aracı kapatmakla aynı şeydir.

## Derleme hattında

1. Her değişiklikte statik analiz, sır taraması ve bağımlılık taraması
   kendiliğinden çalışır.
2. Yeni bir **kritik** bulgu değişikliğin birleştirilmesini engeller.
3. Eski bulgular bir listede izlenir ve önem sırasına göre azaltılır;
   eski borç yüzünden yeni hatalar görmezden gelinmez.
4. İnsan incelemesi araç geçtikten sonra yapılır: inceleyen, aracın
   bulabileceği şeylerle vakit kaybetmez.
