Bitirme projesinde 1232 nesnenin 87'si aynı hücreyi paylaştığı için kayboldu.
Izgarayı sıklaştırmak bunu azaltır mı? Yalnızca veriye bakarak (model
gerekmeden) sayabiliriz:

```python
from dl_data import make_scenes

images, boxes, masks = make_scenes(600, size=32, seed=7)


def lost_objects(grid):
    cell = 32 / grid
    lost = 0
    for scene in boxes:
        taken = set()
        for x1, y1, x2, y2, label in scene:
            key = (int((y1 + y2) / 2 // cell), int((x1 + x2) / 2 // cell))
            lost += key in taken
            taken.add(key)
    return lost


for grid in (2, 4, 8, 16):
    print(grid, grid * grid, lost_objects(grid))
```

```text
2 4 198
4 16 87
8 64 25
16 256 9
```

- 2 × 2'de 198 nesne kayboluyor, 16 × 16'da yalnızca 9.
- Ama sık ızgaranın da bedeli var: 16 × 16'da 256 hücrenin çok azında nesne
  var; nesnellik kaybı neredeyse tamamen "burada nesne yok" demeyi öğrenmekle
  geçer. Her hücre de resmin daha küçük bir parçasını görür.
- Gerçek algılayıcılar iki yolu birleştirir: her hücrede birkaç **çapa**
  (YOLO Mantığı bölümünün notu) ve **birkaç ölçekte ızgara** (büyük nesneler
  kaba ızgarada, küçükler sık ızgarada).
