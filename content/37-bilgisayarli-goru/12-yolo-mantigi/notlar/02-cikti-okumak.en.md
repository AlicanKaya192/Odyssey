The result of a ready-made detection library is usually an object made of
tensors. Turning it into a plain form your own code understands (a list of
dictionaries) makes every later step (filtering, counting, saving) easier.
Let us imitate the same structure without running the real library:

```python
from types import SimpleNamespace

import torch

boxes = SimpleNamespace(
    xyxy=torch.tensor([[10.0, 10, 30, 60], [50, 20, 90, 45]]),
    conf=torch.tensor([0.91, 0.88]),
    cls=torch.tensor([0.0, 2.0]),
)
names = {0: "person", 2: "car"}
rows = []
for box, conf, cls in zip(boxes.xyxy.tolist(), boxes.conf.tolist(), boxes.cls.tolist()):
    rows.append({"name": names[int(cls)], "conf": round(conf, 2), "box": box})
for row in rows:
    print(row)
```

```text
{'name': 'person', 'conf': 0.91, 'box': [10.0, 10.0, 30.0, 60.0]}
{'name': 'car', 'conf': 0.88, 'box': [50.0, 20.0, 90.0, 45.0]}
```

- Class numbers may come as floats (`0.0`); looking up the name in a
  dictionary needs `int(...)`.
- Boxes are pixel coordinates; if you shrank the image before giving it to the
  network, the library usually maps the coordinates back to the original
  image. If you did your own preprocessing, you must do this yourself
  (scaling boxes in the Introduction to Object Detection section).

In the Ultralytics result object the boxes live under `result.boxes` as
`xyxy`, `conf` and `cls`; in tracking mode an `id` comes too. We do not run
the library in this module; check the documentation of the installed version
before using the field names.
