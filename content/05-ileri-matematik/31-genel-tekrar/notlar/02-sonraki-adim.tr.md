İleri Matematik modülünü bitirdin. Yapay zekanın matematik temeli artık elinde; buradan birkaç yol var.

## Makine öğrenmesi patikası

Burada türettiğin formüllerin kodda karşılığı Makine Öğrenmesi
patikasında:

| İleri Matematik modülünde | Kodda |
|---|---|
| normal denklemler, en küçük kareler | doğrusal regresyonun eğitimi |
| sigmoid, log-loss, gradyan | lojistik regresyon |
| entropi, bilgi kazancı | karar ağaçlarında safsızlık |
| standart hata, örnekleme | doğrulama skorlarının dalgalanması |
| kovaryans, PCA | denetimsiz öğrenme ve boyut indirgeme |
| uzaklık, norm | KNN ve kümeleme |

## Kendin yaz

Matematiği pekiştirmenin en iyi yolu onu sıfırdan kodlamak. Yalnızca
NumPy ile:

- doğrusal regresyonu önce normal denklemlerle, sonra gradyan inişiyle
  çöz ve iki sonucu karşılaştır;
- lojistik regresyonu $(p - y)x$ gradyanıyla eğit, log-loss'un düştüğünü
  izle;
- PCA'yı kovaryans matrisinin özvektörleriyle ve SVD ile ayrı ayrı
  hesapla.

## Tekrar için öneriler

- Bir bölümde takıldıysan önce o bölümün **başvuru notuna**, sonra
  **çözümlü örneklerine** dön.
- Tekrar sınavında yanlış yaptığın her soru bir bölüme işaret ediyor;
  Hızlı Başvuru'daki tablolar hangi bölüme gideceğini gösterir.
- Kalkülüs kolu için Türev Kuralları ve Gradyan İnişi, olasılık kolu için
  Koşullu Olasılık ve Bayes ile Örnekleme bölümleri en çok başvurulan
  temeller.
