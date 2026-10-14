| Terim | Anlamı |
|---|---|
| **Üretken model** (generative model) | Verinin dağılımını öğrenen ve ondan yeni örnek üretebilen model |
| **Ayırt edici model** (discriminative model) | Yalnızca "bu örneğin etiketi ne?" sorusunu cevaplayan model, $p(y \mid x)$ |
| **Dağılım** (distribution) | Hangi değerlerin ne sıklıkla görüldüğünün tarifi |
| **Örnekleme** (sampling) | Bir dağılımdan rastgele ama ona uygun değer çekmek |
| **Tohum** (seed) | Rastgele üretecin başlangıç sayısı; aynı tohum aynı sonucu verir |
| **Normal dağılım** (Gaussian) | Ortalama ve kovaryansla belirlenen çan biçimli dağılım |
| **Kovaryans matrisi** | Ölçülerin yayılımı ve birlikte değişimi |
| **Olasılık yoğunluğu** (likelihood) | Bir örneğin bir dağılıma ne kadar uyduğunun ölçüsü |
| **Önsel olasılık** (prior) | Bir sınıfın veriye bakmadan önceki genel oranı |
| **Ezberleme** (memorization) | Modelin eğitim örneklerini neredeyse aynen geri vermesi |
| **En yakın komşu uzaklığı** | Üretilen örneğin eğitim verisindeki en yakın örneğe uzaklığı; 0'a yakınsa kopya |

**Akılda kalsın:**

- Üretken model bir sınıflandırıcı gibi de kullanılabilir; tersi olmaz.
- Üretimde "doğru cevap" yoktur. Tek tek örneklere değil, çok sayıda
  örneğin istatistiğine bakılır.
- Gerçeğe çok benzeyen örnek her zaman iyi değildir: eğitim verisinin
  kopyası olabilir.
- Aynı tohumla aynı örnekler gelir. Çıktıları karşılaştırırken bu yüzden
  tohum sabitlenir.
