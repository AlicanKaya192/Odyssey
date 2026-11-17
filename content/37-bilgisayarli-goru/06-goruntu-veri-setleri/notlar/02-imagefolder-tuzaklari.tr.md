`ImageFolder`'ın üç davranışı sürpriz yaratır. Küçük bir klasörde ölçelim:

```python
from pathlib import Path

import numpy as np
from PIL import Image
from torchvision import datasets

root = Path("pitfalls")
blank = Image.fromarray(np.zeros((4, 4), dtype=np.uint8))
for name in ["2", "10", "9"]:
    (root / name).mkdir(parents=True, exist_ok=True)
    blank.save(root / name / "a.png")
(root / "2" / "notes.txt").write_text("not a picture")
data = datasets.ImageFolder(root)
print(data.classes)
print(len(data))
(root / "empty").mkdir()
try:
    datasets.ImageFolder(root)
except FileNotFoundError as error:
    print(type(error).__name__)
```

```text
['10', '2', '9']
3
FileNotFoundError
```

1. **Sıralama metin sırası:** `"10"`, `"2"`'den önce geliyor; çünkü
   karşılaştırılan sayılar değil harfler. Klasörlere sayı adı veriyorsan
   başına sıfır koy (`02`, `09`, `10`) ya da `class_to_idx`'i kontrol et.
2. **Resim olmayan dosyalar atlanıyor:** `notes.txt` sayılmadı; 3 resim var.
   Ama `.webp` gibi beklenmedik bir uzantı da sessizce atlanabilir; resim
   sayısını her zaman doğrula.
3. **Boş sınıf klasörü hata veriyor:** içinde resim olmayan bir alt klasör
   `FileNotFoundError`'a yol açıyor.

Bir de daha önce gördüğümüz: `ImageFolder` resimleri RGB açar; gri veride
`v2.Grayscale()` gerekir.
