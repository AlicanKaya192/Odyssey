Eğitilen algılayıcıyı bir dosyaya kaydedip başka bir programda yeniden
kurmak için ağırlıklar (`state_dict`) yeter; ağın yapısı kodda
(`make_model`) duruyor. Bu not dersteki eğitilmiş modeli kullanıyor.

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

- Sekiz kayıt: dört evrişim katmanının her birinin ağırlığı ve sapması.
- Yeniden kurulan model aynı resimlere birebir aynı çıktıyı veriyor.
- `TemporaryDirectory` bu deneme için geçici bir klasör açıp `with` bitince
  kendisi kaldırıyor; gerçek projede dosya kalıcı bir yere yazılır.
- Algılayıcıyı kullanırken ağırlıklarla birlikte **ayarlar** da saklanmalı:
  ızgara boyu (`S`), resim boyu, sınıf adları ve sırası, güven eşiği, NMS
  eşiği. Bunlardan biri değişirse aynı ağırlıklar yanlış kutular çizer.
- `weights_only=True` dosyadan yalnızca tensör ve basit yapılar okur;
  başkasından gelen bir dosyada keyfi kod çalışmasını önler.
