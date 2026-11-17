# ImageFolder ve Görüntü Veri Setleri

Şimdiye kadar resimler bellekte hazır bir NumPy dizisi olarak geliyordu.
Gerçek projelerde resimler **dosyadır**: bir klasörde yüzlerce, binlerce
`.png` ya da `.jpg`. En yaygın düzen, her sınıfın kendi alt klasörü
olmasıdır: `train/cat/...`, `train/dog/...`. torchvision'ın **`ImageFolder`**
sınıfı bu düzeni okuyup etiketleri klasör adlarından çıkarıyor. Bu bölümde
şekil resimlerimizi dosyalara yazıp `ImageFolder` ile geri okuyacağız ve
aynı işi kendi `Dataset` sınıfımızla yapacağız.

## Resimleri dosyaya yazmak

Pillow ile her resmi gri tonlu (`"L"` kipi) bir PNG dosyası olarak
kaydediyoruz. Pikselleri önce `uint8`'e çeviriyoruz: dosyada 0–255 tam sayı.
Klasörü çalışma klasörünün içinde, `shapes_data` adıyla açıyoruz.

```python
from pathlib import Path

import numpy as np
from PIL import Image
from dl_data import make_shapes, SHAPES


def save_split(folder, n, seed):
    images, labels = make_shapes(n, seed=seed)
    for i, (img, label) in enumerate(zip(images, labels)):
        target = Path(folder) / SHAPES[label]
        target.mkdir(parents=True, exist_ok=True)
        pixels = (img[0] * 255).round().astype(np.uint8)
        Image.fromarray(pixels, mode="L").save(target / f"{i:03d}.png")


save_split("shapes_data/train", 60, seed=1)
save_split("shapes_data/test", 30, seed=2)
for folder in sorted(Path("shapes_data/train").iterdir()):
    print(folder.name, len(list(folder.glob("*.png"))))
```

```text
circle 24
square 15
triangle 21
```

Artık diskte gerçek bir veri seti var: `shapes_data/train/circle/000.png`
gibi. Klasör adı etiketin kendisi.

## ImageFolder

`ImageFolder` kök klasörü alıyor; her alt klasör bir sınıf, içindeki her
resim bir örnek. `transform` her resme okunurken uygulanıyor.

```python
import torch
from torchvision import datasets
from torchvision.transforms import v2

to_tensor = v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)])
train_set = datasets.ImageFolder("shapes_data/train", transform=to_tensor)
print(train_set.classes)
print(train_set.class_to_idx)
print(len(train_set))
image, label = train_set[0]
print(image.shape, label)
```

```text
['circle', 'square', 'triangle']
{'circle': 0, 'square': 1, 'triangle': 2}
60
torch.Size([3, 16, 16]) 0
```

- `classes` ve `class_to_idx` sınıf adlarını ve numaralarını veriyor;
  numaralar adların **alfabetik** sırasıyla.
- Dikkat: resim `(3, 16, 16)` çıktı. `ImageFolder` dosyaları varsayılan
  olarak **RGB**'ye çevirerek açıyor; gri resim üç aynı kanala dönüşüyor.
- `v2.ToImage()` Pillow resmini tensöre çeviriyor; `ToDtype` [0, 1]'e
  ölçekliyor.

Tek kanal istiyorsak zincire `v2.Grayscale()` ekliyoruz:

```python
gray = v2.Compose([v2.ToImage(), v2.Grayscale(), v2.ToDtype(torch.float32, scale=True)])
train_set = datasets.ImageFolder("shapes_data/train", transform=gray)
test_set = datasets.ImageFolder("shapes_data/test", transform=gray)
image, label = train_set[0]
print(image.shape, len(test_set))
path = Path(train_set.samples[0][0])
print(path.parent.name, path.name)
images, labels = make_shapes(60, seed=1)
original = torch.from_numpy(images[int(path.stem)])
print((image - original).abs().max().item() < 0.01)
```

```text
torch.Size([1, 16, 16]) 30
circle 004.png
True
```

- `train_set.samples` her örneğin dosya yolunu ve etiketini tutuyor. İlk
  örnek `circle` klasörünün ilk dosyası: `make_shapes`'in 4 numaralı
  resmi (ilk dört resim daire değil).
- Dosyadan geri okunan resim, kaydettiğimizle neredeyse aynı. Fark iki
  küçük yuvarlamadan: kaydederken `uint8`'e (en fazla yarım adım) ve
  RGB'den griye dönerken (bir adım; bir adım 1 / 255 ≈ 0,004).

## DataLoader ve doğrulama ayırmak

`ImageFolder` sıradan bir `Dataset`: `DataLoader`'a verilebilir. Eğitim
setinden bir doğrulama parçası ayırmak için `random_split` kullanılır; bölme
tohumlu bir üreteçle tekrarlanabilir.

```python
from torch.utils.data import DataLoader, random_split

part_train, part_val = random_split(train_set, [48, 12],
                                    generator=torch.Generator().manual_seed(0))
loader = DataLoader(part_train, batch_size=16, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
batch, batch_labels = next(iter(loader))
print(len(part_train), len(part_val), len(loader))
print(batch.shape, batch_labels.dtype)
```

```text
48 12 3
torch.Size([16, 1, 16, 16]) torch.int64
```

Yığın `(16, 1, 16, 16)`: önceki bölümlerdeki CNN'ler hiç değişmeden bu
veriyle eğitilebilir. Etiketler `int64`, `CrossEntropyLoss`'un istediği gibi.

## Kendi Dataset sınıfımız

`ImageFolder`'ın içinde olan biten şaşırtıcı derecede kısa. Aynı işi kendimiz
yazalım: dosya yollarını ve etiketleri bir listede topla, istenince dosyayı
aç.

```python
from torch.utils.data import Dataset


class FolderImages(Dataset):
    def __init__(self, root, transform=None):
        self.classes = sorted(p.name for p in Path(root).iterdir() if p.is_dir())
        self.samples = []
        for index, name in enumerate(self.classes):
            for path in sorted((Path(root) / name).glob("*.png")):
                self.samples.append((path, index))
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, i):
        path, label = self.samples[i]
        image = Image.open(path).convert("L")
        if self.transform is not None:
            image = self.transform(image)
        return image, label


mine = FolderImages("shapes_data/train", transform=to_tensor)
print(len(mine), mine.classes, mine[5][0].shape)
mine_files = [p.name for p, _ in mine.samples]
their_files = [Path(p).name for p, _ in train_set.samples]
print(mine_files == their_files, mine[5][1] == train_set[5][1])
print((mine[5][0] - train_set[5][0]).abs().max().item() < 0.005)
```

```text
60 ['circle', 'square', 'triangle'] torch.Size([1, 16, 16])
True True
True
```

- Dosyalar aynı sırada, etiketler aynı. Pikseller en fazla bir `uint8`
  adımı (1 / 255) farklı: `ImageFolder` resmi önce RGB'ye çevirip
  `Grayscale` ile geri griye indiriyor, biz doğrudan gri (`"L"`) açıyoruz.
- Resim `__init__`'te değil, `__getitem__`'da açılıyor: binlerce resim
  belleğe birden yüklenmiyor, yalnızca istenen okunuyor.
- Kendi sınıfını yazmak, etiketler klasör adında değil bir CSV dosyasında
  olduğunda gerekir; notlarda örneği var.

## Özet

- Klasör düzeni: `kök/sınıf/resim.png`; `ImageFolder(kök, transform=...)`.
- Sınıf numaraları klasör adlarının alfabetik sırası; `class_to_idx`'e bak.
- `ImageFolder` resimleri RGB açar; tek kanal için `v2.Grayscale()`.
- Doğrulama ayırmak: `random_split(..., generator=...)`.
- Kendi `Dataset`'in: listede yol ve etiket, dosyayı `__getitem__`'da aç.
