To save the trained detector to a file and rebuild it in another program,
the weights (`state_dict`) are enough; the network's structure lives in the
code (`make_model`). This note uses the trained model from the lesson.

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "shape_detector.pt"
    torch.save(model.state_dict(), path)
    restored = make_model()
    restored.load_state_dict(torch.load(path, weights_only=True))
restored.eval()
with torch.no_grad():
    same = torch.equal(model(x_test[:8]), restored(x_test[:8]))
print(path.name, len(restored.state_dict()), same)
```

```text
shape_detector.pt 8 True
```

- Eight entries: the weight and bias of each of the four convolution layers.
- The rebuilt model gives exactly the same output for the same pictures.
- `TemporaryDirectory` opens a temporary folder for this trial and removes it
  itself when the `with` ends; in a real project the file is written to a
  lasting place.
- When using the detector, **settings** must be kept along with the weights:
  the grid size (`S`), the picture size, the class names and their order, the
  confidence threshold, the NMS threshold. If one of them changes, the same
  weights draw wrong boxes.
- `weights_only=True` reads only tensors and simple structures from the file;
  it prevents arbitrary code from running in a file that came from someone
  else.
