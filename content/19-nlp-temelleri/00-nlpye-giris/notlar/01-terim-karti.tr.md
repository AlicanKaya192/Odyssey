NLP'de sık geçen terimler; patika boyunca bunları kullanacağız.

| Terim | İngilizcesi | Anlamı |
|---|---|---|
| Belge | document | Tek bir metin: bir yorum, bir talep, bir e-posta |
| Derlem | corpus | Belgelerin hepsi: 2000 yorumun tamamı |
| Token | token | Metnin parçalandığı birim; çoğu zaman kelime ya da noktalama |
| Tokenizasyon | tokenisation | Metni token'lara ayırma işi |
| Kelime dağarcığı | vocabulary | Derlemde geçen farklı token'ların listesi |
| Etiket | label | Belgenin doğru cevabı: `positive`, `billing` gibi |
| Durak kelimesi | stop word | Her metinde geçen, tek başına anlam taşımayan kelime: "the", "ve" |
| Taban çizgisi | baseline | Hep en sık sınıfı söyleyen tahmin; her model bunu geçmeli |
| Doğruluk | accuracy | Doğru tahminlerin bütün tahminlere oranı |
| Dengesiz veri | imbalanced data | Sınıfların sayıları çok farklı: 1318 olumlu, 289 nötr |

## Kural mı, öğrenme mi?

| | Kural tabanlı | Öğrenen |
|---|---|---|
| Kim yazar? | Uzman, elle | Model, etiketli örneklerden |
| Anlaşılır mı? | Evet, her kural okunur | Kısmen; ağırlıklara bakmak gerekir |
| Veri ister mi? | Hayır | Evet, etiketli veri |
| Yeni ifadeye uyum | Kural eklenene kadar yok | Benzer örnekler varsa var |
| İyi olduğu yer | Sabit biçimli bilgi: sipariş no, e-posta, tarih | Anlam ve ton: duygu, konu |

İkisi rakip değil. Sipariş numarası gibi biçimi kesin bilgiler için düzenli
ifade (regular expression) yazmak en doğru yol (14. bölüm). Bir yorumun tonu
gibi ince işler için öğrenen model gerekiyor.

## Unutma

- Metinle çalışmaya başlamadan önce veriye bak: kaç belge, etiketler nasıl
  dağılmış, belgeler ne uzunlukta, en sık kelimeler neler.
- Doğruluğu taban çizgisiyle birlikte söyle. "%80 doğruluk" tek başına
  hiçbir şey anlatmaz; sınıfların %85'i aynıysa kötü bir sonuçtur.
