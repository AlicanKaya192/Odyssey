Three behaviours of `ImageFolder` cause surprises. Let us measure them on a
small folder:

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

1. **The order is text order:** `"10"` comes before `"2"`, because letters
   are compared, not numbers. If you give folders number names, put zeros in
   front (`02`, `09`, `10`) or check `class_to_idx`.
2. **Files that are not pictures are skipped:** `notes.txt` was not counted;
   there are 3 pictures. But an unexpected extension such as `.webp` may be
   skipped silently too; always check the number of pictures.
3. **An empty class folder raises an error:** a subfolder with no pictures in
   it leads to a `FileNotFoundError`.

And one we saw before: `ImageFolder` opens pictures as RGB; grey data needs
`v2.Grayscale()`.
