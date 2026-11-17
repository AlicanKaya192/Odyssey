Bu modülün bütün modelleri bir dizüstü bilgisayarın işlemcisinde saniyeler
içinde eğitildi. Bu bilinçli bir seçimdi: her satırı çalıştırıp sonucunu
görebilmek. Gerçek projelerde aynı fikirler daha büyük ölçekte uygulanır.
Buradan sonra gidilebilecek birkaç yön:

## Daha büyük modeller, ekran kartı

- **Ekran kartı:** Performans bölümündeki cihazdan bağımsız kod GPU'da
  değişmeden çalışır; büyük gruplar ve `autocast("cuda", float16)` ile
  eğitim onlarca kat hızlanır.
- **Önceden eğitilmiş modeller:** dil ve görüntü için milyonlarca parametreli
  hazır modeller indirilip ince ayar yapılır. Bu modülde ağırlık
  indirmedik; LoRA bölümündeki fikir tam olarak böyle modeller için.
- **Dağıtık eğitim:** tek bir kartın belleğine sığmayan modeller birden çok
  karta bölünür (`torch.distributed`).

## Daha iyi üretken modeller

- **Difüzyon modelleri:** Üretken YZ Temelleri modülünde fikrini gördük;
  görüntü üretiminde GAN'ların yerini büyük ölçüde aldılar. PyTorch'ta bir
  U-Net ve gürültü takvimiyle kurulur.
- **Dil modelleri:** Gömmeler ve Dil Modelleri modülündeki transformer
  bloğu, üst üste konup çok büyük metinlerle eğitildiğinde bugünkü dil
  modellerinin temelidir.

## Modeli işletmek

- **Model sunmak:** FastAPI ile REST API Yazmak modülündeki "Bir ML
  Modelini Sunmak" bölümü, Tekrarlanabilirlik bölümündeki tahmin
  fonksiyonunu bir web uç noktasına koyar.
- **Paketlemek:** Docker patikası modeli ve bağımlılıklarını bir imaja
  koymayı anlatıyor.
- **İzlemek ve yenilemek:** MLOps ve ML Sistem Tasarımı modülü canlıdaki
  modelin veri kaymasını izlemeyi, yeni sürümü güvenle yayına almayı
  anlatıyor.

## Kendi projen

En iyi sonraki adım kendi verinle küçük bir proje: bir sensör, bir metin
koleksiyonu, bir zaman serisi. Bitirme projesindeki sırayı izle: veriyi tanı,
basit bir kural koy, modeli eğit, doğru ölçüyle değerlendir, teslim paketi
hazırla. Her adımda sonucu ölç; tahmin etme.
