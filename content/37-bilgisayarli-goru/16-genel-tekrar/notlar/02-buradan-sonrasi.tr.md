Bu modülde her şeyi küçük, kendi ürettiğimiz verilerle ve işlemcide yaptık:
fikirler değişmeden kalıyor, ölçek büyüyor. Gerçek projelere geçerken:

## Gerçek veri setleri

- **Sınıflandırma:** MNIST ve Fashion-MNIST (28 × 28 gri), CIFAR-10 (32 × 32
  renkli, 10 sınıf), ImageNet (bin sınıf, milyonlarca resim; hazır ağların
  çoğu onunla eğitildi).
- **Algılama ve bölütleme:** Pascal VOC (20 sınıf), COCO (80 sınıf, kutu ve
  maske; AP ölçüsünün "COCO usulü" çok eşikli hâli buradan).
- `torchvision.datasets` bunların çoğunu tek satırla indiriyor; indirme
  internet ister ve gigabaytlar tutabilir. İndirmeden önce lisansına bak.

## Önceden eğitilmiş ağırlıklar

Bu modülde `resnet18(weights=None)` kullandık. Gerçek projede çoğu zaman
`weights="DEFAULT"` ile ImageNet'te eğitilmiş ağırlıklar indirilir; transfer
öğrenme o zaman asıl gücünü gösterir. O ağırlıkların beklediği ön işleme
(boy, normalleştirme değerleri) ağırlıkla birlikte gelir:
`weights.transforms()`.

## Hazır algılayıcılar ve bölütleyiciler

- `torchvision.models.detection`: Faster R-CNN, RetinaNet, FCOS (çapasız),
  SSD. Çıktıları bu modüldeki biçimde: `boxes` (xyxy), `scores`, `labels`.
- `torchvision.models.segmentation`: FCN, DeepLabV3; örnek bölütleme için
  Mask R-CNN.
- YOLO ailesinin hazır kütüphaneleri hızlıdır ama lisanslarına dikkat et:
  bir kısmı kendi kodunu da açmanı isteyen (AGPL gibi) lisanslarla geliyor.

## Daha hızlı eğitmek

- **GPU:** `model.to("cuda")` ve her toplu veri için `.to("cuda")`. Kod aynı
  kalır; büyük ağlarda onlarca kat hız.
- **Karışık hassasiyet** (`torch.autocast`): bellek yarıya iner, hız artar.
- Veri yüklemeyi paralel yapmak: `DataLoader(..., num_workers=4)`.

## Üretime almak

- Modeli kaydederken ağırlıkların yanında ayarlar: sınıf adları, ön işleme,
  eşikler.
- Başka ortamlarda çalıştırmak için ONNX'e dışa aktarma (`torch.onnx.export`).
- Gerçek dünyada veri kayar (ışık, kamera, mevsim): modeli yeni verilerle
  düzenli ölçmek gerekir. Kestirme şüphesi için Modeli Açıklamak bölümündeki
  yöntemler.

## Sonraki adım

Derin Öğrenme patikasının bir sonraki modülü, **Diziler, Üretken Modeller ve
Dağıtım**, bu modülün üstüne kuruluyor: dizi modelleri, üretken modeller ve
eğitilen bir modeli hızlandırıp dışa aktarmak ve sunmak.
