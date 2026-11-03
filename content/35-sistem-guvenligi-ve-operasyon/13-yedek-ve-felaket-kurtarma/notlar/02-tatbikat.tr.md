Bir felaket kurtarma planı ancak denendiğinde güvenilir olur. Kâğıt
üstünde kusursuz görünen bir plan, ilk tatbikatta eksik bir parolaya, eski
bir telefon numarasına ya da beklenenden çok daha uzun süren bir geri
yüklemeye takılabilir.

## Tatbikat türleri

| Tür | Ne yapılır? | Bedeli |
|---|---|---|
| Masa başı | Ekip bir senaryoyu konuşarak adım adım yürür | Düşük; sistemlere dokunulmaz |
| Kısmi geri yükleme | Bir sistem ya da veri kümesi ayrı bir ortama geri yüklenir | Orta |
| Tam geçiş | Hizmet gerçekten yedek tesise ya da bölgeye taşınır | Yüksek; kesinti riski |

Çoğu kurum masa başı tatbikatla başlar, düzenli kısmi geri yüklemeler
yapar ve tam geçişi daha seyrek dener.

## Tatbikatta neye bakılır?

- Geri yükleme gerçekten **RTO** içinde bitti mi? Süre ölçülür, tahmin
  edilmez.
- Geri gelen veri ne kadar eski? **RPO** tuttu mu?
- Gerekli parolalar, anahtarlar ve belgeler bulunabildi mi? (Sır kasası
  da felakette erişilemez olabilir.)
- Kim neyi yapacağını biliyor muydu? İletişim listesi güncel miydi?
- Bağımlılıklar: veritabanı geri geldi ama ona bağlanan hizmetin
  yapılandırması unutuldu mu?

## Felakette erişilebilirlik

Planın kendisi ve gereken bilgiler, felaketten etkilenecek sistemlerin
**dışında** da saklanır: plan yalnızca çöken sunucudaki bir belgedeyse,
en çok gerektiği an ulaşılamaz. Aynı şekilde yedeklerin şifreleme
anahtarları yedeklerle aynı yerde tutulmaz ama ulaşılabilir bir yerde
tutulur; anahtarı kaybolan şifreli yedek, hiç olmayan yedekle aynıdır.

## Tatbikattan sonra

Her tatbikat, olay sonrası değerlendirme gibi biter: ne iyi gitti, ne
takıldı, hangi düzeltme kimde ve ne zamana kadar (Olay Müdahalesi
bölümü). Plan bu bulgularla güncellenir ve bir sonraki tatbikatta
düzeltmelerin işe yarayıp yaramadığına bakılır.
