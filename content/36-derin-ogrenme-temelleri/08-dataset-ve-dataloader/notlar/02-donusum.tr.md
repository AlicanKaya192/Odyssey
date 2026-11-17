Bir örneği modele vermeden önce değiştirmek (düzleştirmek, çevirmek,
ölçeklemek) çoğu zaman Dataset'in `__getitem__`'ında yapılır. Dönüşümü
bir parametre olarak almak, aynı veri sınıfını farklı işlerde kullanmayı
sağlar:

```python
class TransformedShapes(Dataset):
    def __init__(self, n, transform=None):
        self.images, self.labels = make_shapes(n, size=16)
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, i):
        image = torch.from_numpy(self.images[i])
        if self.transform is not None:
            image = self.transform(image)
        return image, int(self.labels[i])


flat = TransformedShapes(100, transform=lambda t: t.flatten())
mirrored = TransformedShapes(100, transform=lambda t: t.flip(-1))
print(flat[0][0].shape, mirrored[0][0].shape)
print(torch.equal(mirrored[0][0], shapes[0][0].flip(-1)))
```

```text
torch.Size([256]) torch.Size([1, 16, 16])
True
```

- `flat` görüntüyü `nn.Linear`'ın istediği düz vektöre çeviriyor.
- `mirrored` görüntüyü yatayda aynalıyor (son boyutu ters çeviriyor).
  Rastgele uygulanırsa bu, veri artırma (data augmentation) olur: model her
  turda biraz farklı görüntüler görür.
- Dönüşüm her `__getitem__` çağrısında yeniden çalışıyor; asıl veri
  değişmiyor.

Bilgisayarlı Görü modülünde `torchvision.transforms` bu dönüşümlerin hazır
hâllerini veriyor; fikir aynı.
