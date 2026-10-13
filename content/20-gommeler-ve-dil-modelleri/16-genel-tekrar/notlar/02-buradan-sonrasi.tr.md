NLP patikası burada bitiyor. İki modülde metni temizlemekten transformer
bloğuna kadar bütün yolu, her parçayı kendi elinle kurarak yürüdün.
Buradan sonrası birkaç yöne açılıyor.

## Ölçeği büyütmek

Bu modüldeki her şey küçük ve NumPy ile yazıldı; türevleri elle hesapladık.
Gerçek modellerde aynı fikirler **otomatik türev alan** derin öğrenme
kütüphaneleriyle ve ekran kartlarında (GPU) çalışır: geri hesabı kütüphane
yapar, sen yalnızca ileri hesabı yazarsın. Bu modülde elle yazdığın her geri
hesap (08, 09, 10), o kütüphanelerin arka planda ne yaptığını anlamanı
sağlar.

Sırada denenecekler:

- 10'daki dikkat modelini ve 11'deki bloğu bir derin öğrenme kütüphanesiyle
  yeniden yaz ve küçük bir metinde **eğit**: bir karakter düzeyi dil modeli
  iyi bir ilk projedir.
- Önceden eğitilmiş, açık ağırlıklı bir transformer'ın gömmelerini 15'teki
  arama motoruna takıp ölç: 12'deki öğrenme eğrisi nasıl değişiyor?
- Kendi metninle (e-postalar, notlar, bir forum) 15'in adımlarını tekrarla:
  dizin, karma arama, ölçü, eşik, hata analizi.

## Diğer patikalarla bağlantı

| Patika / modül | Bu modülün hangi kısmı |
|---|---|
| Matematik (MAT 2) | vektörler, matris çarpımı, SVD, geri yayılım, entropi |
| ML Algoritmaları | sinir ağının içi, geri yayılım, gradyan inişi |
| Algoritma Teknikleri | dinamik programlama (Viterbi, LCS, ışın araması) |
| Zaman Serileri | dizi modelleri, sıranın önemi |
| API | bir arama motorunu ya da sınıflandırıcıyı hizmet olarak sunmak |
| Büyük Veri | çok büyük metinlerde parça parça sayım |

## Açık sorular

Bu alanın hızla değişen kısmı büyük modellerin kendisi; değişmeyen kısmı bu
modülde gördüğün temeller. Yeni bir yöntemle karşılaştığında aynı soruları
sor:

- Neyi tahmin ederek eğitiliyor? (sonraki kelime, gizlenen kelime, bağlam)
- Metni nasıl parçalıyor ve sırayı nasıl görüyor?
- Neyle ölçülmüş ve o ölçü neyi kaçırıyor?
- Verisi hangi alandan geliyor ve hangi önyargıları taşıyor?
