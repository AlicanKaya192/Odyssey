Birbirini beklemeyen işler aynı anda çalışabilir. `graphlib.TopologicalSorter`
bunu doğrudan destekler: `get_ready()` şu an başlayabilecek **bütün** işleri
verir, `done()` biten işleri bildirir.

```python
from graphlib import TopologicalSorter

deps = {"clean": ["extract"], "validate": ["extract"],
        "features": ["clean", "validate"], "train": ["features"],
        "evaluate": ["train"], "report": ["clean", "evaluate"]}

sorter = TopologicalSorter(deps)
sorter.prepare()
wave = 1
while sorter.is_active():
    ready = sorted(sorter.get_ready())     # şu an hepsi aynı anda çalışabilir
    print("wave", wave, ready)
    sorter.done(*ready)                    # gerçekte: işler bittikçe
    wave += 1
```

```text
wave 1 ['extract']
wave 2 ['clean', 'validate']
wave 3 ['features']
wave 4 ['train']
wave 5 ['evaluate']
wave 6 ['report']
```

İkinci dalgada `clean` ile `validate` aynı anda çalışabilir. Gerçek bir
hatta işler farklı sürelerde biter; `done()` her iş bittiğinde çağrılır ve
`get_ready()` yeni açılan işleri verir. `concurrent.futures` ile birleşince
küçük bir iş zamanlayıcı olur; Airflow'un çekirdeği de bu fikir.
